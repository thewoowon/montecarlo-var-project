"""
Multivariate t-distribution simulation for fat-tail robustness testing
Replaces normal distribution with Student-t to test QMC robustness
"""

import numpy as np
from scipy.stats import t as student_t
from scipy.stats.qmc import Sobol, Halton
from scipy.stats import norm

def mc_sim_tdist(mu, cov, n_sims=10000, df=5):
    """
    Monte Carlo simulation with multivariate t-distribution

    Args:
        mu: Mean vector (d,)
        cov: Covariance matrix (d, d)
        n_sims: Number of scenarios
        df: Degrees of freedom (ν). Lower = fatter tails

    Returns:
        scenarios: (n_sims, d) array of simulated returns
    """
    d = len(mu)

    # Generate standard t-distributed variables
    # Method: Z ~ t_ν for each dimension, then correlate via Cholesky
    Z = student_t.rvs(df=df, size=(n_sims, d))

    # Scale to match Student-t variance
    # Var(t_ν) = ν/(ν-2) for ν > 2
    if df > 2:
        Z = Z * np.sqrt((df - 2) / df)

    # Apply correlation structure via Cholesky
    L = np.linalg.cholesky(cov)
    correlated_Z = Z @ L.T

    # Add mean
    scenarios = mu + correlated_Z

    return scenarios

def qmc_sim_tdist_sobol(mu, cov, n_sims=10000, df=5):
    """
    Quasi-Monte Carlo simulation with Sobol sequence + t-distribution

    Args:
        mu: Mean vector (d,)
        cov: Covariance matrix (d, d)
        n_sims: Number of scenarios
        df: Degrees of freedom

    Returns:
        scenarios: (n_sims, d) array
    """
    d = len(mu)

    # Generate Sobol sequence in [0,1]^d
    sobol = Sobol(d, scramble=True)
    U = sobol.random(n_sims)

    # Transform uniform to t-distributed via inverse CDF
    Z = student_t.ppf(U, df=df)

    # Scale for variance
    if df > 2:
        Z = Z * np.sqrt((df - 2) / df)

    # Apply correlation
    L = np.linalg.cholesky(cov)
    correlated_Z = Z @ L.T

    scenarios = mu + correlated_Z

    return scenarios

def qmc_sim_tdist_halton(mu, cov, n_sims=10000, df=5):
    """
    Quasi-Monte Carlo simulation with Halton sequence + t-distribution
    """
    d = len(mu)

    # Generate Halton sequence
    halton = Halton(d, scramble=True)
    U = halton.random(n_sims)

    # Transform to t-distribution
    Z = student_t.ppf(U, df=df)

    # Scale
    if df > 2:
        Z = Z * np.sqrt((df - 2) / df)

    # Correlate
    L = np.linalg.cholesky(cov)
    correlated_Z = Z @ L.T

    scenarios = mu + correlated_Z

    return scenarios

def qmc_sim_tdist(mu, cov, n_sims=10000, df=5, method='sobol'):
    """
    Unified interface for t-distribution QMC simulation

    Args:
        method: 'sobol' or 'halton'
    """
    if method == 'sobol':
        return qmc_sim_tdist_sobol(mu, cov, n_sims, df)
    elif method == 'halton':
        return qmc_sim_tdist_halton(mu, cov, n_sims, df)
    else:
        raise ValueError(f"Unknown method: {method}")
