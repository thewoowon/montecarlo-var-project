"""
RQ2: Variance Reduction Techniques Analysis
Tests Antithetic Variates and Control Variates effectiveness
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from simulation.mc_sim import mc_sim
from simulation.qmc_sim import qmc_sim
from simulation.variance_reduction import antithetic, control_variate
from var_cvar.var_cvar import var_cvar
import time

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed"
RESULTS_PATH = PROJECT_ROOT / "results" / "simulation"
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

def variance_reduction_experiment(returns, weights, n_sims=10000, n_runs=100, alpha=0.95):
    """
    Compare variance reduction techniques

    Methods tested:
    - MC (baseline)
    - MC + Antithetic
    - MC + Control Variate
    - QMC-Sobol (baseline)
    - QMC-Sobol + Antithetic
    - QMC-Sobol + Control Variate
    """
    print("\n" + "=" * 60)
    print(f"Variance Reduction Analysis (n_sims={n_sims}, n_runs={n_runs})")
    print("=" * 60)

    mu = returns.mean().values
    cov = returns.cov().values
    control_mean = np.dot(mu, weights)  # Expected portfolio return

    results = {
        'method': [],
        'var_mean': [],
        'var_std': [],
        'var_reduction': [],
        'cvar_mean': [],
        'cvar_std': [],
        'cvar_reduction': [],
        'time_mean': []
    }

    # Baseline MC
    print("\n[1/6] Running MC (baseline)...")
    vars_mc, cvars_mc, times_mc = run_simulation('mc', mu, cov, weights, n_sims, n_runs, alpha)
    baseline_var_std = np.std(vars_mc)
    baseline_cvar_std = np.std(cvars_mc)

    results['method'].append('MC')
    results['var_mean'].append(np.mean(vars_mc))
    results['var_std'].append(baseline_var_std)
    results['var_reduction'].append(0.0)
    results['cvar_mean'].append(np.mean(cvars_mc))
    results['cvar_std'].append(baseline_cvar_std)
    results['cvar_reduction'].append(0.0)
    results['time_mean'].append(np.mean(times_mc))
    print(f"  VaR Std: {baseline_var_std:.6f}")

    # MC + Antithetic
    print("\n[2/6] Running MC + Antithetic...")
    vars_list, cvars_list, times_list = [], [], []

    for run in range(n_runs):
        t_start = time.time()

        # Generate half scenarios, use antithetic for the other half
        Z = np.random.randn(n_sims // 2, len(mu))
        Z_anti = antithetic(Z)

        L = np.linalg.cholesky(cov)
        scenarios = mu + Z_anti @ L.T

        portfolio_ret = scenarios @ weights
        var_val, cvar_val = var_cvar(portfolio_ret, alpha)

        vars_list.append(var_val)
        cvars_list.append(cvar_val)
        times_list.append(time.time() - t_start)

    var_std = np.std(vars_list)
    cvar_std = np.std(cvars_list)
    var_reduction = (1 - var_std / baseline_var_std) * 100

    results['method'].append('MC + Antithetic')
    results['var_mean'].append(np.mean(vars_list))
    results['var_std'].append(var_std)
    results['var_reduction'].append(var_reduction)
    results['cvar_mean'].append(np.mean(cvars_list))
    results['cvar_std'].append(cvar_std)
    results['cvar_reduction'].append((1 - cvar_std / baseline_cvar_std) * 100)
    results['time_mean'].append(np.mean(times_list))
    print(f"  VaR Std: {var_std:.6f}, Reduction: {var_reduction:.2f}%")

    # MC + Control Variate
    print("\n[3/6] Running MC + Control Variate...")
    vars_list, cvars_list, times_list = [], [], []

    for run in range(n_runs):
        t_start = time.time()

        scenarios = mc_sim(mu, cov, n_sims)
        portfolio_ret_raw = scenarios @ weights

        # Apply control variate (use portfolio expected return as control)
        control = portfolio_ret_raw  # The return itself
        portfolio_ret_adjusted = control_variate(portfolio_ret_raw, control, control_mean)

        var_val, cvar_val = var_cvar(portfolio_ret_adjusted, alpha)

        vars_list.append(var_val)
        cvars_list.append(cvar_val)
        times_list.append(time.time() - t_start)

    var_std = np.std(vars_list)
    cvar_std = np.std(cvars_list)
    var_reduction = (1 - var_std / baseline_var_std) * 100

    results['method'].append('MC + Control Variate')
    results['var_mean'].append(np.mean(vars_list))
    results['var_std'].append(var_std)
    results['var_reduction'].append(var_reduction)
    results['cvar_mean'].append(np.mean(cvars_list))
    results['cvar_std'].append(cvar_std)
    results['cvar_reduction'].append((1 - cvar_std / baseline_cvar_std) * 100)
    results['time_mean'].append(np.mean(times_list))
    print(f"  VaR Std: {var_std:.6f}, Reduction: {var_reduction:.2f}%")

    # QMC baseline
    print("\n[4/6] Running QMC-Sobol (baseline)...")
    vars_qmc, cvars_qmc, times_qmc = run_simulation('qmc', mu, cov, weights, n_sims, n_runs, alpha)
    qmc_var_std = np.std(vars_qmc)
    qmc_cvar_std = np.std(cvars_qmc)

    results['method'].append('QMC-Sobol')
    results['var_mean'].append(np.mean(vars_qmc))
    results['var_std'].append(qmc_var_std)
    results['var_reduction'].append((1 - qmc_var_std / baseline_var_std) * 100)
    results['cvar_mean'].append(np.mean(cvars_qmc))
    results['cvar_std'].append(qmc_cvar_std)
    results['cvar_reduction'].append((1 - qmc_cvar_std / baseline_cvar_std) * 100)
    results['time_mean'].append(np.mean(times_qmc))
    print(f"  VaR Std: {qmc_var_std:.6f}")

    # QMC + Antithetic
    print("\n[5/6] Running QMC-Sobol + Antithetic...")
    vars_list, cvars_list, times_list = [], [], []

    for run in range(n_runs):
        t_start = time.time()

        scenarios = qmc_sim(mu, cov, n_sims // 2, method='sobol')
        Z = (scenarios - mu) @ np.linalg.inv(np.linalg.cholesky(cov)).T
        Z_anti = antithetic(Z)

        L = np.linalg.cholesky(cov)
        scenarios_anti = mu + Z_anti @ L.T

        portfolio_ret = scenarios_anti @ weights
        var_val, cvar_val = var_cvar(portfolio_ret, alpha)

        vars_list.append(var_val)
        cvars_list.append(cvar_val)
        times_list.append(time.time() - t_start)

    var_std = np.std(vars_list)
    cvar_std = np.std(cvars_list)

    results['method'].append('QMC-Sobol + Antithetic')
    results['var_mean'].append(np.mean(vars_list))
    results['var_std'].append(var_std)
    results['var_reduction'].append((1 - var_std / baseline_var_std) * 100)
    results['cvar_mean'].append(np.mean(cvars_list))
    results['cvar_std'].append(cvar_std)
    results['cvar_reduction'].append((1 - cvar_std / baseline_cvar_std) * 100)
    results['time_mean'].append(np.mean(times_list))
    print(f"  VaR Std: {var_std:.6f}")

    # QMC + Control Variate
    print("\n[6/6] Running QMC-Sobol + Control Variate...")
    vars_list, cvars_list, times_list = [], [], []

    for run in range(n_runs):
        t_start = time.time()

        scenarios = qmc_sim(mu, cov, n_sims, method='sobol')
        portfolio_ret_raw = scenarios @ weights
        portfolio_ret_adjusted = control_variate(portfolio_ret_raw, portfolio_ret_raw, control_mean)

        var_val, cvar_val = var_cvar(portfolio_ret_adjusted, alpha)

        vars_list.append(var_val)
        cvars_list.append(cvar_val)
        times_list.append(time.time() - t_start)

    var_std = np.std(vars_list)
    cvar_std = np.std(cvars_list)

    results['method'].append('QMC-Sobol + Control Variate')
    results['var_mean'].append(np.mean(vars_list))
    results['var_std'].append(var_std)
    results['var_reduction'].append((1 - var_std / baseline_var_std) * 100)
    results['cvar_mean'].append(np.mean(cvars_list))
    results['cvar_std'].append(cvar_std)
    results['cvar_reduction'].append((1 - cvar_std / baseline_cvar_std) * 100)
    results['time_mean'].append(np.mean(times_list))
    print(f"  VaR Std: {var_std:.6f}")

    df_results = pd.DataFrame(results)
    df_results.to_csv(RESULTS_PATH / "variance_reduction_results.csv", index=False)

    print("\n✅ Variance reduction experiment complete!")
    print(f"Results saved to: {RESULTS_PATH / 'variance_reduction_results.csv'}")

    return df_results

def run_simulation(sim_type, mu, cov, weights, n_sims, n_runs, alpha):
    """Helper function to run baseline simulations"""
    vars_list, cvars_list, times_list = [], [], []

    for run in range(n_runs):
        t_start = time.time()

        if sim_type == 'mc':
            scenarios = mc_sim(mu, cov, n_sims)
        else:
            scenarios = qmc_sim(mu, cov, n_sims, method='sobol')

        portfolio_ret = scenarios @ weights
        var_val, cvar_val = var_cvar(portfolio_ret, alpha)

        vars_list.append(var_val)
        cvars_list.append(cvar_val)
        times_list.append(time.time() - t_start)

    return vars_list, cvars_list, times_list

def plot_variance_reduction(df_results, save_path=None):
    """Plot variance reduction comparison"""
    if save_path is None:
        save_path = PROJECT_ROOT / "plots"
        save_path.mkdir(exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # VaR Standard Deviation
    ax = axes[0]
    ax.barh(df_results['method'], df_results['var_std'], color='steelblue', alpha=0.7)
    ax.set_xlabel('VaR Standard Deviation')
    ax.set_title('VaR Estimation Variance by Method')
    ax.grid(True, alpha=0.3, axis='x')

    # Variance Reduction %
    ax = axes[1]
    colors = ['gray' if x == 0 else ('green' if x > 0 else 'red') for x in df_results['var_reduction']]
    ax.barh(df_results['method'], df_results['var_reduction'], color=colors, alpha=0.7)
    ax.set_xlabel('Variance Reduction (%)')
    ax.set_title('Variance Reduction vs MC Baseline')
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig(save_path / "variance_reduction.png", dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {save_path / 'variance_reduction.png'}")
    plt.close()

def main():
    print("=" * 60)
    print("Variance Reduction Techniques Analysis")
    print("=" * 60)

    # Load returns
    returns = pd.read_csv(DATA_PATH / "returns.csv", index_col=0, parse_dates=True)
    weights = np.array([1/3, 1/3, 1/3])

    # Run experiment
    df_results = variance_reduction_experiment(
        returns=returns,
        weights=weights,
        n_sims=10000,
        n_runs=100,
        alpha=0.95
    )

    # Plot results
    plot_variance_reduction(df_results)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY: Variance Reduction Performance")
    print("=" * 60)
    print(df_results[['method', 'var_std', 'var_reduction']].to_string(index=False))

if __name__ == "__main__":
    main()
