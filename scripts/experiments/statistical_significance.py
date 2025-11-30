"""
Statistical Significance Testing for MC vs QMC
Implements Bootstrap confidence intervals and McNemar test
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
from scipy import stats
sys.path.append(str(Path(__file__).parent.parent))

from simulation.mc_sim import mc_sim
from simulation.qmc_sim import qmc_sim
from var_cvar.var_cvar import var_cvar

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed"
RESULTS_PATH = PROJECT_ROOT / "results" / "simulation"
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

def bootstrap_var_comparison(returns, weights, n_sims=10000, n_bootstrap=100, alpha=0.95):
    """
    Bootstrap analysis to test if MC vs QMC differences are statistically significant

    Returns 95% confidence intervals for VaR estimates
    """
    print("\n" + "=" * 60)
    print("Bootstrap Confidence Interval Analysis")
    print("=" * 60)
    print(f"n_simulations: {n_sims}, n_bootstrap: {n_bootstrap}")

    mu = returns.mean().values
    cov = returns.cov().values

    results = {
        'method': [],
        'var_mean': [],
        'var_std': [],
        'var_ci_lower': [],
        'var_ci_upper': [],
        'cvar_mean': [],
        'cvar_std': [],
        'cvar_ci_lower': [],
        'cvar_ci_upper': []
    }

    methods = [
        ('MC', 'mc'),
        ('QMC-Sobol', 'sobol'),
        ('QMC-Halton', 'halton')
    ]

    for method_name, method_type in methods:
        print(f"\n{method_name}:")
        vars_bootstrap = []
        cvars_bootstrap = []

        for i in range(n_bootstrap):
            if method_type == 'mc':
                scenarios = mc_sim(mu, cov, n_sims)
            else:
                scenarios = qmc_sim(mu, cov, n_sims, method=method_type)

            portfolio_ret = scenarios @ weights
            var_val, cvar_val = var_cvar(portfolio_ret, alpha)
            vars_bootstrap.append(var_val)
            cvars_bootstrap.append(cvar_val)

            if (i + 1) % 20 == 0:
                print(f"  Progress: {i+1}/{n_bootstrap}")

        vars_arr = np.array(vars_bootstrap)
        cvars_arr = np.array(cvars_bootstrap)

        # 95% confidence interval
        var_ci = np.percentile(vars_arr, [2.5, 97.5])
        cvar_ci = np.percentile(cvars_arr, [2.5, 97.5])

        results['method'].append(method_name)
        results['var_mean'].append(np.mean(vars_arr))
        results['var_std'].append(np.std(vars_arr))
        results['var_ci_lower'].append(var_ci[0])
        results['var_ci_upper'].append(var_ci[1])
        results['cvar_mean'].append(np.mean(cvars_arr))
        results['cvar_std'].append(np.std(cvars_arr))
        results['cvar_ci_lower'].append(cvar_ci[0])
        results['cvar_ci_upper'].append(cvar_ci[1])

        print(f"  VaR:  {np.mean(vars_arr):.6f} [{var_ci[0]:.6f}, {var_ci[1]:.6f}]")
        print(f"  CVaR: {np.mean(cvars_arr):.6f} [{cvar_ci[0]:.6f}, {cvar_ci[1]:.6f}]")

    df_results = pd.DataFrame(results)

    # Check if confidence intervals overlap
    print("\n" + "=" * 60)
    print("Confidence Interval Overlap Analysis")
    print("=" * 60)

    mc_ci = (df_results.loc[df_results['method']=='MC', 'var_ci_lower'].values[0],
             df_results.loc[df_results['method']=='MC', 'var_ci_upper'].values[0])

    for method in ['QMC-Sobol', 'QMC-Halton']:
        qmc_ci = (df_results.loc[df_results['method']==method, 'var_ci_lower'].values[0],
                  df_results.loc[df_results['method']==method, 'var_ci_upper'].values[0])

        overlap = max(0, min(mc_ci[1], qmc_ci[1]) - max(mc_ci[0], qmc_ci[0]))

        if overlap == 0:
            significance = "✅ SIGNIFICANT (no overlap)"
        else:
            significance = "❌ NOT SIGNIFICANT (overlap detected)"

        print(f"\nMC vs {method}:")
        print(f"  MC CI:  [{mc_ci[0]:.6f}, {mc_ci[1]:.6f}]")
        print(f"  QMC CI: [{qmc_ci[0]:.6f}, {qmc_ci[1]:.6f}]")
        print(f"  Overlap: {overlap:.6f}")
        print(f"  {significance}")

    return df_results

def mcnemar_test_backtesting(backtest_df):
    """
    McNemar test for paired comparison of VaR violations

    Tests if MC and QMC have significantly different failure rates
    on the same days
    """
    print("\n" + "=" * 60)
    print("McNemar Test: Paired Violation Comparison")
    print("=" * 60)

    # Create binary violation indicators
    mc_violations = (backtest_df['actual_return'] < backtest_df['var_mc']).astype(int)
    sobol_violations = (backtest_df['actual_return'] < backtest_df['var_qmc_sobol']).astype(int)
    halton_violations = (backtest_df['actual_return'] < backtest_df['var_qmc_halton']).astype(int)

    results = []

    # MC vs QMC-Sobol
    print("\nMC vs QMC-Sobol:")
    n_both_fail = np.sum((mc_violations == 1) & (sobol_violations == 1))
    n_only_mc = np.sum((mc_violations == 1) & (sobol_violations == 0))
    n_only_sobol = np.sum((mc_violations == 0) & (sobol_violations == 1))
    n_both_pass = np.sum((mc_violations == 0) & (sobol_violations == 0))

    print(f"  Both fail:     {n_both_fail}")
    print(f"  Only MC fails: {n_only_mc}")
    print(f"  Only QMC fails: {n_only_sobol}")
    print(f"  Both pass:     {n_both_pass}")

    # McNemar statistic
    if n_only_mc + n_only_sobol > 0:
        mcnemar_stat = (abs(n_only_mc - n_only_sobol) - 1)**2 / (n_only_mc + n_only_sobol)
        p_value = 1 - stats.chi2.cdf(mcnemar_stat, df=1)
    else:
        mcnemar_stat = 0
        p_value = 1.0

    print(f"  McNemar χ²: {mcnemar_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")

    if p_value < 0.05:
        print(f"  ✅ SIGNIFICANT difference (p < 0.05)")
    else:
        print(f"  ❌ NOT SIGNIFICANT (p ≥ 0.05)")

    results.append({
        'comparison': 'MC vs QMC-Sobol',
        'both_fail': n_both_fail,
        'only_method1': n_only_mc,
        'only_method2': n_only_sobol,
        'both_pass': n_both_pass,
        'mcnemar_stat': mcnemar_stat,
        'p_value': p_value,
        'significant': p_value < 0.05
    })

    # MC vs QMC-Halton
    print("\nMC vs QMC-Halton:")
    n_both_fail = np.sum((mc_violations == 1) & (halton_violations == 1))
    n_only_mc = np.sum((mc_violations == 1) & (halton_violations == 0))
    n_only_halton = np.sum((mc_violations == 0) & (halton_violations == 1))
    n_both_pass = np.sum((mc_violations == 0) & (halton_violations == 0))

    print(f"  Both fail:     {n_both_fail}")
    print(f"  Only MC fails: {n_only_mc}")
    print(f"  Only QMC fails: {n_only_halton}")
    print(f"  Both pass:     {n_both_pass}")

    if n_only_mc + n_only_halton > 0:
        mcnemar_stat = (abs(n_only_mc - n_only_halton) - 1)**2 / (n_only_mc + n_only_halton)
        p_value = 1 - stats.chi2.cdf(mcnemar_stat, df=1)
    else:
        mcnemar_stat = 0
        p_value = 1.0

    print(f"  McNemar χ²: {mcnemar_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")

    if p_value < 0.05:
        print(f"  ✅ SIGNIFICANT difference (p < 0.05)")
    else:
        print(f"  ❌ NOT SIGNIFICANT (p ≥ 0.05)")

    results.append({
        'comparison': 'MC vs QMC-Halton',
        'both_fail': n_both_fail,
        'only_method1': n_only_mc,
        'only_method2': n_only_halton,
        'both_pass': n_both_pass,
        'mcnemar_stat': mcnemar_stat,
        'p_value': p_value,
        'significant': p_value < 0.05
    })

    return pd.DataFrame(results)

def plot_bootstrap_ci(df_bootstrap, save_path=None):
    """Plot bootstrap confidence intervals"""
    if save_path is None:
        save_path = PROJECT_ROOT / "plots"
        save_path.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    methods = df_bootstrap['method'].values
    means = df_bootstrap['var_mean'].values
    lower = df_bootstrap['var_ci_lower'].values
    upper = df_bootstrap['var_ci_upper'].values

    y_pos = np.arange(len(methods))

    # Plot confidence intervals
    for i in range(len(methods)):
        ax.plot([lower[i], upper[i]], [i, i], 'o-', linewidth=2, markersize=8,
                label=methods[i])
        ax.plot(means[i], i, 'D', markersize=10, color='red')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods)
    ax.set_xlabel('VaR (95% Confidence Interval)')
    ax.set_title('Bootstrap Confidence Intervals: MC vs QMC')
    ax.grid(True, alpha=0.3, axis='x')
    ax.legend(['CI Range', 'Mean'], loc='upper right')

    plt.tight_layout()
    plt.savefig(save_path / "bootstrap_confidence_intervals.png", dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path / 'bootstrap_confidence_intervals.png'}")
    plt.close()

def main():
    print("=" * 60)
    print("Statistical Significance Testing")
    print("=" * 60)

    # Load data
    returns = pd.read_csv(DATA_PATH / "returns.csv", index_col=0, parse_dates=True)
    weights = np.array([1/3, 1/3, 1/3])

    # Bootstrap analysis
    df_bootstrap = bootstrap_var_comparison(
        returns=returns,
        weights=weights,
        n_sims=10000,
        n_bootstrap=100,
        alpha=0.95
    )

    df_bootstrap.to_csv(RESULTS_PATH / "bootstrap_confidence_intervals.csv", index=False)
    print(f"\nBootstrap results saved to: {RESULTS_PATH / 'bootstrap_confidence_intervals.csv'}")

    # Plot
    plot_bootstrap_ci(df_bootstrap)

    # McNemar test (if backtest data exists)
    backtest_path = PROJECT_ROOT / "results" / "backtesting" / "backtest_full.csv"
    if backtest_path.exists():
        print("\n" + "=" * 60)
        print("Loading backtesting data for McNemar test...")
        print("=" * 60)

        backtest_df = pd.read_csv(backtest_path, index_col=0, parse_dates=True)
        df_mcnemar = mcnemar_test_backtesting(backtest_df)

        df_mcnemar.to_csv(RESULTS_PATH / "mcnemar_test_results.csv", index=False)
        print(f"\nMcNemar results saved to: {RESULTS_PATH / 'mcnemar_test_results.csv'}")
    else:
        print("\n⚠️  Backtest data not found. Run stress_backtesting.py first.")

    print("\n✅ Statistical significance testing complete!")

if __name__ == "__main__":
    main()
