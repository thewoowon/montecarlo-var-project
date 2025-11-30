import numpy as np
from scipy.stats import norm
from scipy.stats.qmc import Sobol, Halton

def qmc_sim_sobol(mu, cov, n_sims=10000):
    """Quasi-Monte Carlo simulation using Sobol sequence"""
    d = len(mu)
    sobol = Sobol(d, scramble=True)
    U = sobol.random(n_sims)
    Z = norm.ppf(U)
    L = np.linalg.cholesky(cov)
    return mu + Z @ L.T

def qmc_sim_halton(mu, cov, n_sims=10000):
    """Quasi-Monte Carlo simulation using Halton sequence"""
    d = len(mu)
    halton = Halton(d, scramble=True)
    U = halton.random(n_sims)
    Z = norm.ppf(U)
    L = np.linalg.cholesky(cov)
    return mu + Z @ L.T

def qmc_sim(mu, cov, n_sims=10000, method='sobol'):
    """
    Quasi-Monte Carlo simulation with selectable sequence

    Parameters:
    -----------
    mu : array-like, shape (d,)
        Mean vector
    cov : array-like, shape (d, d)
        Covariance matrix
    n_sims : int
        Number of scenarios
    method : str, {'sobol', 'halton'}
        QMC sequence type

    Returns:
    --------
    scenarios : ndarray, shape (n_sims, d)
        Simulated scenarios
    """
    if method == 'sobol':
        return qmc_sim_sobol(mu, cov, n_sims)
    elif method == 'halton':
        return qmc_sim_halton(mu, cov, n_sims)
    else:
        raise ValueError(f"Unknown method: {method}. Use 'sobol' or 'halton'.")
