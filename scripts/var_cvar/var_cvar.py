import numpy as np

def var_cvar(losses, alpha=0.95):
    VaR = np.quantile(losses, 1 - alpha)
    CVaR = losses[losses <= VaR].mean()
    return VaR, CVaR
