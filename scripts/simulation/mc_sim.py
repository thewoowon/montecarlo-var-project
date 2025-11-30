import numpy as np

def mc_sim(mu, cov, n_sims=10000):
    d = len(mu)
    Z = np.random.randn(n_sims, d)
    L = np.linalg.cholesky(cov)
    return mu + Z @ L.T
