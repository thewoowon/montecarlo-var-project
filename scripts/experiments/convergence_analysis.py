"""
RQ1 & RQ3: MC vs QMC Convergence Analysis
Compares convergence speed and accuracy across different simulation counts
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
import time

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed"
RESULTS_PATH = PROJECT_ROOT / "results" / "simulation"
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

def compute_reference_var(returns, weights, n_ref=100000, alpha=0.95):
    """Compute high-accuracy reference VaR using large MC simulation"""
    mu = returns.mean().values
    cov = returns.cov().values

    portfolio_returns = []
    for _ in range(5):  # Average over 5 runs for stability
        scenarios = mc_sim(mu, cov, n_ref)
        portfolio_ret = scenarios @ weights
        portfolio_returns.extend(portfolio_ret)

    var_ref, cvar_ref = var_cvar(np.array(portfolio_returns), alpha)
    return var_ref, cvar_ref

def convergence_experiment(returns, weights, n_simulations_list, n_runs=50, alpha=0.95):
    """
    Test convergence of MC vs QMC methods

    Parameters:
    -----------
    returns : DataFrame
        Historical returns
    weights : array
        Portfolio weights
    n_simulations_list : list
        List of simulation counts to test
    n_runs : int
        Number of independent runs for each simulation count
    alpha : float
        VaR confidence level
    """
    print("Computing reference VaR with large MC simulation...")
    var_ref, cvar_ref = compute_reference_var(returns, weights, n_ref=100000, alpha=alpha)
    print(f"Reference VaR: {var_ref:.6f}, CVaR: {cvar_ref:.6f}")

    mu = returns.mean().values
    cov = returns.cov().values

    results = {
        'n_sims': [],
        'method': [],
        'var_mean': [],
        'var_std': [],
        'cvar_mean': [],
        'cvar_std': [],
        'var_rmse': [],
        'cvar_rmse': [],
        'time_mean': [],
        'time_std': []
    }

    methods = [
        ('MC', 'mc'),
        ('QMC-Sobol', 'sobol'),
        ('QMC-Halton', 'halton')
    ]

    for n_sims in n_simulations_list:
        print(f"\nTesting n_sims={n_sims}...")

        for method_name, method_type in methods:
            vars_list = []
            cvars_list = []
            times_list = []

            for run in range(n_runs):
                t_start = time.time()

                if method_type == 'mc':
                    scenarios = mc_sim(mu, cov, n_sims)
                else:
                    scenarios = qmc_sim(mu, cov, n_sims, method=method_type.split('-')[-1].lower())

                portfolio_ret = scenarios @ weights
                var_val, cvar_val = var_cvar(portfolio_ret, alpha)

                t_end = time.time()

                vars_list.append(var_val)
                cvars_list.append(cvar_val)
                times_list.append(t_end - t_start)

            vars_arr = np.array(vars_list)
            cvars_arr = np.array(cvars_list)

            var_rmse = np.sqrt(np.mean((vars_arr - var_ref)**2))
            cvar_rmse = np.sqrt(np.mean((cvars_arr - cvar_ref)**2))

            results['n_sims'].append(n_sims)
            results['method'].append(method_name)
            results['var_mean'].append(np.mean(vars_arr))
            results['var_std'].append(np.std(vars_arr))
            results['cvar_mean'].append(np.mean(cvars_arr))
            results['cvar_std'].append(np.std(cvars_arr))
            results['var_rmse'].append(var_rmse)
            results['cvar_rmse'].append(cvar_rmse)
            results['time_mean'].append(np.mean(times_list))
            results['time_std'].append(np.std(times_list))

            print(f"  {method_name:15s}: VaR RMSE={var_rmse:.6f}, Time={np.mean(times_list):.4f}s")

    df_results = pd.DataFrame(results)
    df_results.to_csv(RESULTS_PATH / "convergence_results.csv", index=False)

    print("\n✅ Convergence experiment complete!")
    print(f"Results saved to: {RESULTS_PATH / 'convergence_results.csv'}")

    return df_results

def plot_convergence(df_results, save_path=None):
    """Plot convergence analysis results"""
    if save_path is None:
        save_path = PROJECT_ROOT / "plots"
        save_path.mkdir(exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    methods = df_results['method'].unique()
    colors = {'MC': 'blue', 'QMC-Sobol': 'red', 'QMC-Halton': 'green'}

    # VaR RMSE vs n_sims
    ax = axes[0, 0]
    for method in methods:
        data = df_results[df_results['method'] == method]
        ax.loglog(data['n_sims'], data['var_rmse'], 'o-',
                 label=method, color=colors[method], linewidth=2)
    ax.set_xlabel('Number of Simulations')
    ax.set_ylabel('VaR RMSE')
    ax.set_title('VaR Convergence: RMSE vs Simulation Count')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # CVaR RMSE vs n_sims
    ax = axes[0, 1]
    for method in methods:
        data = df_results[df_results['method'] == method]
        ax.loglog(data['n_sims'], data['cvar_rmse'], 'o-',
                 label=method, color=colors[method], linewidth=2)
    ax.set_xlabel('Number of Simulations')
    ax.set_ylabel('CVaR RMSE')
    ax.set_title('CVaR Convergence: RMSE vs Simulation Count')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # VaR Standard Deviation
    ax = axes[1, 0]
    for method in methods:
        data = df_results[df_results['method'] == method]
        ax.loglog(data['n_sims'], data['var_std'], 'o-',
                 label=method, color=colors[method], linewidth=2)
    ax.set_xlabel('Number of Simulations')
    ax.set_ylabel('VaR Standard Deviation')
    ax.set_title('VaR Variance: Std Dev vs Simulation Count')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Computation Time
    ax = axes[1, 1]
    for method in methods:
        data = df_results[df_results['method'] == method]
        ax.semilogx(data['n_sims'], data['time_mean'], 'o-',
                   label=method, color=colors[method], linewidth=2)
    ax.set_xlabel('Number of Simulations')
    ax.set_ylabel('Computation Time (seconds)')
    ax.set_title('Computational Efficiency')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path / "convergence_analysis.png", dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {save_path / 'convergence_analysis.png'}")
    plt.close()

def main():
    print("=" * 60)
    print("Convergence Analysis: MC vs QMC")
    print("=" * 60)

    # Load returns
    returns = pd.read_csv(DATA_PATH / "returns.csv", index_col=0, parse_dates=True)
    print(f"\nLoaded returns: {returns.shape}")
    print(f"Assets: {returns.columns.tolist()}")

    # Portfolio weights (equal weight)
    weights = np.array([1/3, 1/3, 1/3])
    print(f"Portfolio weights: {weights}")

    # Simulation counts to test
    n_simulations_list = [100, 500, 1000, 2000, 5000, 10000, 20000]

    # Run experiment
    df_results = convergence_experiment(
        returns=returns,
        weights=weights,
        n_simulations_list=n_simulations_list,
        n_runs=50,
        alpha=0.95
    )

    # Plot results
    plot_convergence(df_results)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY: VaR RMSE at n=10000")
    print("=" * 60)
    summary = df_results[df_results['n_sims'] == 10000][['method', 'var_rmse', 'cvar_rmse', 'time_mean']]
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
