"""
RQ4: Stress Period Backtesting Analysis
Tests MC vs QMC VaR performance during Korean market crises:
- 2020 COVID crash
- 2022 Legoland crisis
- 2023 Interest rate surge
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from simulation.mc_sim import mc_sim
from simulation.qmc_sim import qmc_sim
from var_cvar.var_cvar import var_cvar
from backtesting.kupiec_test import kupiec_test, christoffersen_test, conditional_coverage_test

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed"
RESULTS_PATH = PROJECT_ROOT / "results" / "backtesting"
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

# Define stress periods (Korean market crises)
STRESS_PERIODS = {
    'COVID-19 Crash': ('2020-02-01', '2020-04-30'),
    'Legoland Crisis': ('2022-09-01', '2022-12-31'),
    'Rate Surge 2023': ('2023-01-01', '2023-06-30'),
    'Full Period': ('2020-01-01', '2024-12-31')
}

def rolling_var_backtest(returns, weights, window=252, alpha=0.95, n_sims=10000):
    """
    Rolling window VaR backtesting

    Parameters:
    -----------
    returns : DataFrame
        Historical returns
    weights : array
        Portfolio weights
    window : int
        Rolling window size (default 252 = 1 year)
    alpha : float
        VaR confidence level
    n_sims : int
        Number of simulations

    Returns:
    --------
    backtest_results : DataFrame
        Backtesting results with VaR estimates and violations
    """
    methods = ['MC', 'QMC-Sobol', 'QMC-Halton']

    backtest_data = {
        'date': [],
        'actual_return': [],
        'var_mc': [],
        'var_qmc_sobol': [],
        'var_qmc_halton': []
    }

    print(f"Running rolling backtests (window={window})...")

    for i in range(window, len(returns)):
        date = returns.index[i]
        train_returns = returns.iloc[i-window:i]

        # Actual portfolio return on day i
        actual_return = (returns.iloc[i].values @ weights).item()

        # Estimate mu and cov from training window
        mu = train_returns.mean().values
        cov = train_returns.cov().values

        # Estimate VaR with each method
        # MC
        scenarios_mc = mc_sim(mu, cov, n_sims)
        portfolio_mc = scenarios_mc @ weights
        var_mc, _ = var_cvar(portfolio_mc, alpha)

        # QMC-Sobol
        scenarios_sobol = qmc_sim(mu, cov, n_sims, method='sobol')
        portfolio_sobol = scenarios_sobol @ weights
        var_sobol, _ = var_cvar(portfolio_sobol, alpha)

        # QMC-Halton
        scenarios_halton = qmc_sim(mu, cov, n_sims, method='halton')
        portfolio_halton = scenarios_halton @ weights
        var_halton, _ = var_cvar(portfolio_halton, alpha)

        backtest_data['date'].append(date)
        backtest_data['actual_return'].append(actual_return)
        backtest_data['var_mc'].append(var_mc)
        backtest_data['var_qmc_sobol'].append(var_sobol)
        backtest_data['var_qmc_halton'].append(var_halton)

        if (i - window) % 100 == 0:
            print(f"  Progress: {i - window}/{len(returns) - window}")

    df_backtest = pd.DataFrame(backtest_data)
    df_backtest['date'] = pd.to_datetime(df_backtest['date'])
    df_backtest.set_index('date', inplace=True)

    return df_backtest

def analyze_violations(df_backtest, alpha=0.95):
    """
    Analyze VaR violations and run statistical tests

    Parameters:
    -----------
    df_backtest : DataFrame
        Backtesting results
    alpha : float
        VaR confidence level

    Returns:
    --------
    results : DataFrame
        Summary statistics for each method
    """
    methods = {
        'MC': 'var_mc',
        'QMC-Sobol': 'var_qmc_sobol',
        'QMC-Halton': 'var_qmc_halton'
    }

    results = {
        'method': [],
        'violations': [],
        'violation_rate': [],
        'expected_rate': [],
        'kupiec_LR': [],
        'kupiec_pval': [],
        'christoffersen_LR': [],
        'christoffersen_pval': [],
        'conditional_cov_LR': [],
        'conditional_cov_pval': []
    }

    expected_rate = 1 - alpha
    n = len(df_backtest)

    for method_name, var_col in methods.items():
        # Check violations (actual return < VaR)
        violations_binary = (df_backtest['actual_return'] < df_backtest[var_col]).astype(int)
        violations_count = violations_binary.sum()
        violation_rate = violations_count / n

        # Kupiec test
        lr_uc, pval_uc = kupiec_test(violations_count, n, alpha)

        # Christoffersen independence test
        lr_ind, pval_ind = christoffersen_test(violations_binary.values)

        # Conditional coverage test
        lr_cc, pval_cc = conditional_coverage_test(violations_binary.values, n, alpha)

        results['method'].append(method_name)
        results['violations'].append(violations_count)
        results['violation_rate'].append(violation_rate)
        results['expected_rate'].append(expected_rate)
        results['kupiec_LR'].append(lr_uc)
        results['kupiec_pval'].append(pval_uc)
        results['christoffersen_LR'].append(lr_ind)
        results['christoffersen_pval'].append(pval_ind)
        results['conditional_cov_LR'].append(lr_cc)
        results['conditional_cov_pval'].append(pval_cc)

    return pd.DataFrame(results)

def stress_period_analysis(df_backtest, alpha=0.95):
    """
    Analyze VaR performance during stress periods

    Parameters:
    -----------
    df_backtest : DataFrame
        Full backtesting results
    alpha : float
        VaR confidence level

    Returns:
    --------
    stress_results : dict
        Results for each stress period
    """
    stress_results = {}

    for period_name, (start, end) in STRESS_PERIODS.items():
        print(f"\nAnalyzing stress period: {period_name} ({start} to {end})")

        # Filter data for stress period
        mask = (df_backtest.index >= start) & (df_backtest.index <= end)
        df_period = df_backtest[mask]

        if len(df_period) == 0:
            print(f"  No data available for {period_name}")
            continue

        print(f"  Sample size: {len(df_period)} days")

        # Analyze violations for this period
        results_period = analyze_violations(df_period, alpha)
        stress_results[period_name] = results_period

        print(f"\n  Violation Rates:")
        for _, row in results_period.iterrows():
            print(f"    {row['method']:15s}: {row['violations']:3d} ({row['violation_rate']*100:.2f}%)")

    return stress_results

def plot_stress_backtest(df_backtest, stress_results, save_path=None):
    """Plot backtesting results with stress periods highlighted"""
    if save_path is None:
        save_path = PROJECT_ROOT / "plots"
        save_path.mkdir(exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(16, 10))

    # Plot 1: VaR estimates over time
    ax = axes[0]
    ax.plot(df_backtest.index, df_backtest['actual_return'], 'k-', alpha=0.3, linewidth=0.5, label='Actual Return')
    ax.plot(df_backtest.index, df_backtest['var_mc'], 'b-', linewidth=1, label='MC VaR')
    ax.plot(df_backtest.index, df_backtest['var_qmc_sobol'], 'r-', linewidth=1, label='QMC-Sobol VaR')
    ax.plot(df_backtest.index, df_backtest['var_qmc_halton'], 'g-', linewidth=1, label='QMC-Halton VaR')

    # Highlight stress periods
    colors_stress = ['red', 'orange', 'purple']
    for i, (period_name, (start, end)) in enumerate(STRESS_PERIODS.items()):
        if period_name != 'Full Period':
            ax.axvspan(pd.to_datetime(start), pd.to_datetime(end),
                      alpha=0.2, color=colors_stress[i % len(colors_stress)], label=period_name)

    ax.set_ylabel('Portfolio Return / VaR')
    ax.set_title('Rolling VaR Backtesting with Stress Periods')
    ax.legend(loc='lower left')
    ax.grid(True, alpha=0.3)

    # Plot 2: Violation rates by stress period
    ax = axes[1]
    if stress_results:
        period_names = list(stress_results.keys())
        x = np.arange(len(period_names))
        width = 0.25

        for i, method in enumerate(['MC', 'QMC-Sobol', 'QMC-Halton']):
            violation_rates = [stress_results[p][stress_results[p]['method'] == method]['violation_rate'].values[0] * 100
                             for p in period_names]
            ax.bar(x + i*width, violation_rates, width, label=method)

        ax.axhline(5, color='red', linestyle='--', linewidth=2, label='Expected 5%')
        ax.set_ylabel('Violation Rate (%)')
        ax.set_title('VaR Violation Rates by Stress Period')
        ax.set_xticks(x + width)
        ax.set_xticklabels(period_names, rotation=15, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(save_path / "stress_backtesting.png", dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path / 'stress_backtesting.png'}")
    plt.close()

def main():
    print("=" * 60)
    print("Stress Period Backtesting Analysis")
    print("=" * 60)

    # Load returns
    returns = pd.read_csv(DATA_PATH / "returns.csv", index_col=0, parse_dates=True)
    weights = np.array([1/3, 1/3, 1/3])

    print(f"\nData period: {returns.index[0]} to {returns.index[-1]}")
    print(f"Total observations: {len(returns)}")

    # Run rolling backtest
    df_backtest = rolling_var_backtest(
        returns=returns,
        weights=weights,
        window=252,
        alpha=0.95,
        n_sims=10000
    )

    # Save full backtest results
    df_backtest.to_csv(RESULTS_PATH / "backtest_full.csv")
    print(f"\nBacktest results saved to: {RESULTS_PATH / 'backtest_full.csv'}")

    # Analyze violations for full period
    print("\n" + "=" * 60)
    print("FULL PERIOD ANALYSIS")
    print("=" * 60)
    results_full = analyze_violations(df_backtest, alpha=0.95)
    print(results_full.to_string(index=False))
    results_full.to_csv(RESULTS_PATH / "backtest_full_summary.csv", index=False)

    # Analyze stress periods
    print("\n" + "=" * 60)
    print("STRESS PERIOD ANALYSIS")
    print("=" * 60)
    stress_results = stress_period_analysis(df_backtest, alpha=0.95)

    # Save stress period results
    for period_name, results in stress_results.items():
        filename = period_name.replace(' ', '_').replace('-', '').lower()
        results.to_csv(RESULTS_PATH / f"backtest_{filename}.csv", index=False)

    # Plot results
    plot_stress_backtest(df_backtest, stress_results)

    print("\n✅ Stress backtesting analysis complete!")

if __name__ == "__main__":
    main()
