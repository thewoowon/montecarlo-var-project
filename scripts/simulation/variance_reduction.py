import numpy as np

def antithetic(Z):
    return np.vstack([Z, -Z])

def control_variate(loss, control, control_mean):
    beta = np.cov(loss, control)[0,1] / np.var(control)
    adjusted = loss - beta * (control - control_mean)
    return adjusted
