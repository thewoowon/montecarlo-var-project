"""
RQ5: Boundary Condition Analysis
Identifies conditions where QMC outperforms or underperforms MC
Tests: asset dimension, volatility levels, correlation structure, simulation count
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

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed"
RESULTS_PATH = PROJECT_ROOT / "results" / "simulation"
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

def test_dimension_effect(base_mu, base_cov, n_sims=10000, n_runs=50, alpha=0.95):
    """
    Test: How does asset dimension affect MC vs QMC performance?

    We'll test dimensions: 2, 3, 5, 10, 15
    """
    print("\n" + "=" * 60)
    print("TEST 1: Effect of Asset Dimension")
    print("=" * 60)

    dimensions = [2, 3, 5, 10, 15]
    results = {
        'dimension': [],
        'method': [],
        'var_std': [],
        'var_rmse': [],
        'relative_efficiency': []
    }

    for d in dimensions:
        print(f"\nTesting dimension d={d}...")

        # Create d-dimensional problem by replicating/scaling base assets
        if d <= len(base_mu):
            mu = base_mu[:d]
            cov = base_cov[:d, :d]
        else:
            # Extend by replicating with small perturbations
            mu = np.tile(base_mu, d // len(base_mu) + 1)[:d]
            cov_base = base_cov
            cov = np.eye(d) * np.mean(np.diag(cov_base))
            # Add some correlation structure
            for i in range(d):
                for j in range(i+1, d):
                    cov[i, j] = cov[j, i] = 0.3 * cov[i, i]

        weights = np.ones(d) / d

        # Compute reference VaR
        portfolio_returns_ref = []
        for _ in range(10):
            scenarios = mc_sim(mu, cov, 50000)
            portfolio_returns_ref.extend(scenarios @ weights)
        var_ref, _ = var_cvar(np.array(portfolio_returns_ref), alpha)

        # Test MC
        vars_mc = []
        for _ in range(n_runs):
            scenarios = mc_sim(mu, cov, n_sims)
            portfolio_ret = scenarios @ weights
            var_val, _ = var_cvar(portfolio_ret, alpha)
            vars_mc.append(var_val)

        mc_std = np.std(vars_mc)
        mc_rmse = np.sqrt(np.mean((np.array(vars_mc) - var_ref)**2))

        results['dimension'].append(d)
        results['method'].append('MC')
        results['var_std'].append(mc_std)
        results['var_rmse'].append(mc_rmse)
        results['relative_efficiency'].append(1.0)

        # Test QMC-Sobol
        vars_qmc = []
        for _ in range(n_runs):
            scenarios = qmc_sim(mu, cov, n_sims, method='sobol')
            portfolio_ret = scenarios @ weights
            var_val, _ = var_cvar(portfolio_ret, alpha)
            vars_qmc.append(var_val)

        qmc_std = np.std(vars_qmc)
        qmc_rmse = np.sqrt(np.mean((np.array(vars_qmc) - var_ref)**2))
        efficiency = mc_std / qmc_std

        results['dimension'].append(d)
        results['method'].append('QMC-Sobol')
        results['var_std'].append(qmc_std)
        results['var_rmse'].append(qmc_rmse)
        results['relative_efficiency'].append(efficiency)

        print(f"  MC   Std: {mc_std:.6f}, RMSE: {mc_rmse:.6f}")
        print(f"  QMC  Std: {qmc_std:.6f}, RMSE: {qmc_rmse:.6f}")
        print(f"  Efficiency Gain: {(efficiency - 1) * 100:.2f}%")

    return pd.DataFrame(results)

def test_volatility_effect(base_mu, base_cov, n_sims=10000, n_runs=50, alpha=0.95):
    """
    Test: How does volatility level affect MC vs QMC performance?

    We'll scale covariance by different factors
    """
    print("\n" + "=" * 60)
    print("TEST 2: Effect of Volatility Level")
    print("=" * 60)

    vol_scales = [0.5, 1.0, 1.5, 2.0, 3.0]  # Scale volatility
    results = {
        'vol_scale': [],
        'method': [],
        'var_std': [],
        'relative_efficiency': []
    }

    weights = np.ones(len(base_mu)) / len(base_mu)

    for scale in vol_scales:
        print(f"\nTesting volatility scale={scale}...")

        mu = base_mu
        cov = base_cov * scale

        # Reference VaR
        portfolio_returns_ref = []
        for _ in range(10):
            scenarios = mc_sim(mu, cov, 50000)
            portfolio_returns_ref.extend(scenarios @ weights)
        var_ref, _ = var_cvar(np.array(portfolio_returns_ref), alpha)

        # MC
        vars_mc = []
        for _ in range(n_runs):
            scenarios = mc_sim(mu, cov, n_sims)
            portfolio_ret = scenarios @ weights
            var_val, _ = var_cvar(portfolio_ret, alpha)
            vars_mc.append(var_val)

        mc_std = np.std(vars_mc)

        results['vol_scale'].append(scale)
        results['method'].append('MC')
        results['var_std'].append(mc_std)
        results['relative_efficiency'].append(1.0)

        # QMC
        vars_qmc = []
        for _ in range(n_runs):
            scenarios = qmc_sim(mu, cov, n_sims, method='sobol')
            portfolio_ret = scenarios @ weights
            var_val, _ = var_cvar(portfolio_ret, alpha)
            vars_qmc.append(var_val)

        qmc_std = np.std(vars_qmc)
        efficiency = mc_std / qmc_std

        results['vol_scale'].append(scale)
        results['method'].append('QMC-Sobol')
        results['var_std'].append(qmc_std)
        results['relative_efficiency'].append(efficiency)

        print(f"  MC   Std: {mc_std:.6f}")
        print(f"  QMC  Std: {qmc_std:.6f}")
        print(f"  Efficiency Gain: {(efficiency - 1) * 100:.2f}%")

    return pd.DataFrame(results)

def test_correlation_effect(base_mu, base_cov, n_sims=10000, n_runs=50, alpha=0.95):
    """
    Test: How does correlation structure affect MC vs QMC?

    We'll test different correlation levels
    """
    print("\n" + "=" * 60)
    print("TEST 3: Effect of Correlation Structure")
    print("=" * 60)

    correlation_levels = [0.1, 0.3, 0.5, 0.7, 0.9]
    results = {
        'correlation': [],
        'method': [],
        'var_std': [],
        'relative_efficiency': []
    }

    d = len(base_mu)
    weights = np.ones(d) / d
    vol = np.sqrt(np.diag(base_cov))

    for corr in correlation_levels:
        print(f"\nTesting correlation={corr}...")

        # Build covariance with target correlation
        cov = np.eye(d)
        for i in range(d):
            for j in range(d):
                if i != j:
                    cov[i, j] = corr
        # Scale by volatilities
        for i in range(d):
            for j in range(d):
                cov[i, j] *= vol[i] * vol[j]

        mu = base_mu

        # Reference
        portfolio_returns_ref = []
        for _ in range(10):
            scenarios = mc_sim(mu, cov, 50000)
            portfolio_returns_ref.extend(scenarios @ weights)
        var_ref, _ = var_cvar(np.array(portfolio_returns_ref), alpha)

        # MC
        vars_mc = []
        for _ in range(n_runs):
            scenarios = mc_sim(mu, cov, n_sims)
            portfolio_ret = scenarios @ weights
            var_val, _ = var_cvar(portfolio_ret, alpha)
            vars_mc.append(var_val)

        mc_std = np.std(vars_mc)

        results['correlation'].append(corr)
        results['method'].append('MC')
        results['var_std'].append(mc_std)
        results['relative_efficiency'].append(1.0)

        # QMC
        vars_qmc = []
        for _ in range(n_runs):
            scenarios = qmc_sim(mu, cov, n_sims, method='sobol')
            portfolio_ret = scenarios @ weights
            var_val, _ = var_cvar(portfolio_ret, alpha)
            vars_qmc.append(var_val)

        qmc_std = np.std(vars_qmc)
        efficiency = mc_std / qmc_std

        results['correlation'].append(corr)
        results['method'].append('QMC-Sobol')
        results['var_std'].append(qmc_std)
        results['relative_efficiency'].append(efficiency)

        print(f"  MC   Std: {mc_std:.6f}")
        print(f"  QMC  Std: {qmc_std:.6f}")
        print(f"  Efficiency Gain: {(efficiency - 1) * 100:.2f}%")

    return pd.DataFrame(results)

def plot_boundary_conditions(df_dim, df_vol, df_corr, save_path=None):
    """Plot boundary condition analysis results"""
    if save_path is None:
        save_path = PROJECT_ROOT / "plots"
        save_path.mkdir(exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Dimension effect
    ax = axes[0, 0]
    for method in df_dim['method'].unique():
        data = df_dim[df_dim['method'] == method]
        ax.plot(data['dimension'], data['var_std'], 'o-', label=method, linewidth=2)
    ax.set_xlabel('Asset Dimension')
    ax.set_ylabel('VaR Standard Deviation')
    ax.set_title('Effect of Asset Dimension on VaR Estimation')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Dimension efficiency
    ax = axes[0, 1]
    qmc_data = df_dim[df_dim['method'] == 'QMC-Sobol']
    ax.plot(qmc_data['dimension'], qmc_data['relative_efficiency'], 'ro-', linewidth=2)
    ax.axhline(1.0, color='black', linestyle='--', label='MC Baseline')
    ax.set_xlabel('Asset Dimension')
    ax.set_ylabel('Relative Efficiency (MC_std / QMC_std)')
    ax.set_title('QMC Efficiency Gain vs Dimension')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Volatility effect
    ax = axes[1, 0]
    for method in df_vol['method'].unique():
        data = df_vol[df_vol['method'] == method]
        ax.plot(data['vol_scale'], data['var_std'], 'o-', label=method, linewidth=2)
    ax.set_xlabel('Volatility Scale Factor')
    ax.set_ylabel('VaR Standard Deviation')
    ax.set_title('Effect of Volatility Level on VaR Estimation')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Correlation effect
    ax = axes[1, 1]
    qmc_data = df_corr[df_corr['method'] == 'QMC-Sobol']
    ax.plot(qmc_data['correlation'], qmc_data['relative_efficiency'], 'ro-', linewidth=2)
    ax.axhline(1.0, color='black', linestyle='--', label='MC Baseline')
    ax.set_xlabel('Correlation Level')
    ax.set_ylabel('Relative Efficiency (MC_std / QMC_std)')
    ax.set_title('QMC Efficiency Gain vs Correlation')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path / "boundary_conditions.png", dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path / 'boundary_conditions.png'}")
    plt.close()

def main():
    print("=" * 60)
    print("Boundary Condition Analysis")
    print("=" * 60)

    # Load base data
    returns = pd.read_csv(DATA_PATH / "returns.csv", index_col=0, parse_dates=True)
    base_mu = returns.mean().values
    base_cov = returns.cov().values

    print(f"\nBase asset dimension: {len(base_mu)}")
    print(f"Base volatility (annualized): {np.sqrt(np.diag(base_cov) * 252)}")

    # Run tests
    df_dimension = test_dimension_effect(base_mu, base_cov, n_sims=10000, n_runs=50)
    df_dimension.to_csv(RESULTS_PATH / "boundary_dimension.csv", index=False)

    df_volatility = test_volatility_effect(base_mu, base_cov, n_sims=10000, n_runs=50)
    df_volatility.to_csv(RESULTS_PATH / "boundary_volatility.csv", index=False)

    df_correlation = test_correlation_effect(base_mu, base_cov, n_sims=10000, n_runs=50)
    df_correlation.to_csv(RESULTS_PATH / "boundary_correlation.csv", index=False)

    # Plot results
    plot_boundary_conditions(df_dimension, df_volatility, df_correlation)

    print("\n" + "=" * 60)
    print("BOUNDARY CONDITION SUMMARY")
    print("=" * 60)
    print("\nKey Findings:")
    print("1. QMC efficiency by dimension:")
    qmc_eff = df_dimension[df_dimension['method'] == 'QMC-Sobol']['relative_efficiency'].values
    dims = df_dimension[df_dimension['method'] == 'QMC-Sobol']['dimension'].values
    for d, eff in zip(dims, qmc_eff):
        print(f"   d={d:2d}: {(eff-1)*100:+.1f}% gain")

    print("\n✅ Boundary condition analysis complete!")

if __name__ == "__main__":
    main()
