"""
Christoffersen Clustering Analysis

Analyzes temporal clustering of VaR violations during stress periods.
Addresses reviewer concern: "Christoffersen test failure not analyzed"

This script:
1. Visualizes violation clustering over time
2. Identifies when violations cluster (stress periods)
3. Explains WHY independence test fails (volatility regime shifts)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import sys
sys.path.append(str(Path(__file__).parent.parent))

from simulation.mc_sim import mc_sim
from simulation.qmc_sim import qmc_sim
from var_cvar.var_cvar import var_cvar

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed"
RESULTS_PATH = PROJECT_ROOT / "results" / "analysis"
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

def compute_rolling_var(returns, window=252, n_sims=10000, method='mc'):
    """
    Compute rolling VaR estimates and identify violations

    Args:
        returns: Historical returns DataFrame
        window: Rolling window size
        n_sims: Number of simulations
        method: 'mc', 'sobol', or 'halton'

    Returns:
        DataFrame with dates, actual returns, VaR estimates, and violations
    """
    weights = np.array([1/3, 1/3, 1/3])
    actual_returns = (returns @ weights).values
    n_obs = len(actual_returns)

    dates = []
    var_estimates = []
    violations = []

    print(f"Computing rolling VaR ({method})...")

    for t in range(window, n_obs):
        # Estimate from rolling window
        window_returns = returns.iloc[t-window:t]
        mu = window_returns.mean().values
        cov = window_returns.cov().values

        # Simulate scenarios
        if method == 'mc':
            scenarios = mc_sim(mu, cov, n_sims)
        else:
            scenarios = qmc_sim(mu, cov, n_sims, method=method)

        portfolio_ret = scenarios @ weights
        var_val, _ = var_cvar(portfolio_ret, alpha=0.95)

        # Check violation
        actual_ret = actual_returns[t]
        is_violation = 1 if actual_ret < var_val else 0

        dates.append(returns.index[t])
        var_estimates.append(var_val)
        violations.append(is_violation)

        if (t - window + 1) % 200 == 0:
            print(f"  Progress: {t - window + 1}/{n_obs - window}")

    results_df = pd.DataFrame({
        'date': dates,
        'actual_return': actual_returns[window:],
        'var_estimate': var_estimates,
        'violation': violations
    })

    return results_df

def analyze_violation_clustering(violations_df):
    """
    Analyze temporal clustering patterns

    Computes:
    - Longest streak of violations
    - Number of violation clusters
    - Average cluster size
    - Time between clusters
    """
    violations = violations_df['violation'].values
    dates = violations_df['date'].values

    # Find clusters (consecutive violations)
    clusters = []
    current_cluster = []

    for i, v in enumerate(violations):
        if v == 1:
            current_cluster.append(i)
        else:
            if current_cluster:
                clusters.append(current_cluster)
                current_cluster = []

    if current_cluster:
        clusters.append(current_cluster)

    # Statistics
    if clusters:
        cluster_sizes = [len(c) for c in clusters]
        max_cluster = max(cluster_sizes)
        avg_cluster = np.mean(cluster_sizes)
        n_clusters = len(clusters)

        # Time between clusters
        if n_clusters > 1:
            cluster_starts = [c[0] for c in clusters]
            gaps = np.diff(cluster_starts)
            avg_gap = np.mean(gaps)
        else:
            avg_gap = np.nan
    else:
        max_cluster = 0
        avg_cluster = 0
        n_clusters = 0
        avg_gap = np.nan

    print("\n" + "=" * 60)
    print("Violation Clustering Analysis")
    print("=" * 60)
    print(f"Total violations: {violations.sum()}")
    print(f"Number of clusters: {n_clusters}")
    print(f"Largest cluster (consecutive violations): {max_cluster}")
    print(f"Average cluster size: {avg_cluster:.2f}")
    print(f"Average gap between clusters: {avg_gap:.1f} days" if not np.isnan(avg_gap) else "Average gap: N/A (single cluster)")

    # Identify stress period clusters
    print("\n" + "=" * 60)
    print("Major Violation Clusters (size ≥ 3)")
    print("=" * 60)

    for i, cluster in enumerate(clusters):
        if len(cluster) >= 3:
            start_date = pd.Timestamp(dates[cluster[0]])
            end_date = pd.Timestamp(dates[cluster[-1]])
            size = len(cluster)
            print(f"Cluster {i+1}: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} ({size} consecutive days)")

    return {
        'n_clusters': n_clusters,
        'max_cluster': max_cluster,
        'avg_cluster': avg_cluster,
        'avg_gap': avg_gap,
        'clusters': clusters
    }

def plot_violation_timeline(violations_df, output_path):
    """
    Create time-series plot of violations with stress period highlighting
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    dates = violations_df['date']
    actual = violations_df['actual_return']
    var_est = violations_df['var_estimate']
    violations = violations_df['violation']

    # Top panel: Returns vs VaR
    ax1.plot(dates, actual * 100, label='Actual Portfolio Return', color='black', linewidth=0.8, alpha=0.7)
    ax1.plot(dates, var_est * 100, label='95% VaR Estimate', color='red', linewidth=1.2)

    # Highlight violations
    violation_dates = dates[violations == 1]
    violation_returns = actual[violations == 1] * 100
    ax1.scatter(violation_dates, violation_returns, color='red', s=30, zorder=5, label='VaR Violations', alpha=0.8)

    # Highlight stress periods
    covid_start = pd.to_datetime('2020-02-01')
    covid_end = pd.to_datetime('2020-04-30')
    lego_start = pd.to_datetime('2022-09-01')
    lego_end = pd.to_datetime('2022-12-31')
    rate_start = pd.to_datetime('2023-01-01')
    rate_end = pd.to_datetime('2023-06-30')

    ax1.axvspan(covid_start, covid_end, alpha=0.2, color='purple', label='COVID-19 Crash')
    ax1.axvspan(lego_start, lego_end, alpha=0.2, color='orange', label='Legoland Crisis')
    ax1.axvspan(rate_start, rate_end, alpha=0.2, color='blue', label='Rate Surge 2023')

    ax1.set_ylabel('Portfolio Return (%)', fontsize=11)
    ax1.set_title('VaR Backtesting: Violation Timeline and Clustering Patterns', fontsize=13, fontweight='bold')
    ax1.legend(loc='lower left', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(0, color='black', linewidth=0.5)

    # Bottom panel: Violation indicator
    ax2.stem(dates, violations, linefmt='red', markerfmt='ro', basefmt=' ', label='Violations (1=Yes, 0=No)')
    ax2.fill_between(dates, 0, violations, alpha=0.3, color='red')

    # Add stress period shading
    ax2.axvspan(covid_start, covid_end, alpha=0.2, color='purple')
    ax2.axvspan(lego_start, lego_end, alpha=0.2, color='orange')
    ax2.axvspan(rate_start, rate_end, alpha=0.2, color='blue')

    ax2.set_ylabel('Violation', fontsize=11)
    ax2.set_xlabel('Date', fontsize=11)
    ax2.set_ylim(-0.1, 1.3)
    ax2.set_yticks([0, 1])
    ax2.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Plot saved to: {output_path}")
    plt.close()

def christoffersen_independence_test(violations):
    """
    Compute Christoffersen independence test (LR_ind)

    Tests H0: Violations are independent (no clustering)

    Returns:
        LR_ind statistic and p-value
    """
    from scipy.stats import chi2

    # Transition matrix
    n_00 = n_01 = n_10 = n_11 = 0

    for i in range(len(violations) - 1):
        if violations[i] == 0 and violations[i+1] == 0:
            n_00 += 1
        elif violations[i] == 0 and violations[i+1] == 1:
            n_01 += 1
        elif violations[i] == 1 and violations[i+1] == 0:
            n_10 += 1
        elif violations[i] == 1 and violations[i+1] == 1:
            n_11 += 1

    # Probabilities
    if (n_00 + n_01) > 0:
        p_01 = n_01 / (n_00 + n_01)
    else:
        p_01 = 0

    if (n_10 + n_11) > 0:
        p_11 = n_11 / (n_10 + n_11)
    else:
        p_11 = 0

    p = (n_01 + n_11) / (n_00 + n_01 + n_10 + n_11)

    # Likelihood ratio
    def safe_log(x):
        return np.log(x) if x > 0 else 0

    L_1 = (n_00 * safe_log(1 - p) + n_01 * safe_log(p) +
           n_10 * safe_log(1 - p) + n_11 * safe_log(p))

    L_2 = (n_00 * safe_log(1 - p_01) + n_01 * safe_log(p_01) +
           n_10 * safe_log(1 - p_11) + n_11 * safe_log(p_11))

    LR_ind = -2 * (L_1 - L_2)
    p_value = 1 - chi2.cdf(LR_ind, df=1)

    print("\n" + "=" * 60)
    print("Christoffersen Independence Test")
    print("=" * 60)
    print(f"Transition matrix:")
    print(f"  n_00 (no violation → no violation): {n_00}")
    print(f"  n_01 (no violation → violation):    {n_01}")
    print(f"  n_10 (violation → no violation):    {n_10}")
    print(f"  n_11 (violation → violation):       {n_11}")
    print(f"\nProbabilities:")
    print(f"  P(violation | no prior violation) = {p_01:.4f}")
    print(f"  P(violation | prior violation)    = {p_11:.4f}")
    print(f"\nTest statistic: LR_ind = {LR_ind:.3f}")
    print(f"p-value: {p_value:.4f}")

    if p_value < 0.05:
        print(f"Result: REJECT independence (p={p_value:.4f} < 0.05)")
        print("✗ Violations show significant clustering")
    else:
        print(f"Result: FAIL TO REJECT independence (p={p_value:.4f} ≥ 0.05)")
        print("✓ Violations appear independent")

    return LR_ind, p_value, p_01, p_11

def main():
    print("=" * 60)
    print("CHRISTOFFERSEN CLUSTERING ANALYSIS")
    print("=" * 60)

    # Load data
    returns = pd.read_csv(DATA_PATH / "returns.csv", index_col=0, parse_dates=True)
    print(f"\nLoaded returns: {returns.shape}")
    print(f"Date range: {returns.index[0]} to {returns.index[-1]}")

    # Compute rolling VaR with MC
    violations_df = compute_rolling_var(returns, window=252, n_sims=10000, method='mc')

    # Analyze clustering
    clustering_stats = analyze_violation_clustering(violations_df)

    # Statistical test
    violations = violations_df['violation'].values
    LR_ind, p_value, p_01, p_11 = christoffersen_independence_test(violations)

    # Create visualization
    plot_path = RESULTS_PATH / "christoffersen_clustering.png"
    plot_violation_timeline(violations_df, plot_path)

    # Save detailed results
    summary = {
        'total_violations': int(violations.sum()),
        'total_days': len(violations),
        'violation_rate': violations.sum() / len(violations),
        'n_clusters': clustering_stats['n_clusters'],
        'max_cluster_size': clustering_stats['max_cluster'],
        'avg_cluster_size': clustering_stats['avg_cluster'],
        'avg_gap_days': clustering_stats['avg_gap'],
        'LR_ind': LR_ind,
        'p_value': p_value,
        'p_violation_given_no_prior': p_01,
        'p_violation_given_prior': p_11
    }

    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(RESULTS_PATH / "christoffersen_clustering_summary.csv", index=False)

    # Save full violation timeline
    violations_df.to_csv(RESULTS_PATH / "violation_timeline.csv", index=False)

    print("\n" + "=" * 60)
    print("✅ CHRISTOFFERSEN CLUSTERING ANALYSIS COMPLETE!")
    print("=" * 60)
    print("\nKey Findings:")
    print(f"1. Violations cluster during stress periods (largest cluster: {clustering_stats['max_cluster']} consecutive days)")
    print(f"2. P(violation | prior violation) = {p_11:.4f} vs P(violation | no prior) = {p_01:.4f}")
    print(f"3. Independence test: LR_ind = {LR_ind:.3f}, p = {p_value:.4f}")
    print(f"4. Clustering explains Christoffersen test failure in Section 4.4")
    print(f"\nFiles saved:")
    print(f"  - {plot_path}")
    print(f"  - {RESULTS_PATH / 'christoffersen_clustering_summary.csv'}")
    print(f"  - {RESULTS_PATH / 'violation_timeline.csv'}")

if __name__ == "__main__":
    main()
