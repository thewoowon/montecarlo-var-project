import numpy as np
from scipy import stats

def kupiec_test(violations, n, alpha=0.95):
    """
    Kupiec's unconditional coverage test (LR_uc)

    H0: The observed failure rate equals the expected failure rate

    Parameters:
    -----------
    violations : int
        Number of VaR violations
    n : int
        Total number of observations
    alpha : float
        VaR confidence level (e.g., 0.95 for 95% VaR)

    Returns:
    --------
    LR_uc : float
        Likelihood ratio statistic
    p_value : float
        P-value from chi-squared distribution with 1 df
    """
    if violations == 0:
        violations = 1e-10  # Avoid log(0)

    pi = violations / n
    expected_rate = 1 - alpha

    LR_uc = -2 * (
        np.log((1-expected_rate)**(n-violations) * expected_rate**violations)
        - np.log((1-pi)**(n-violations) * pi**violations)
    )

    p_value = 1 - stats.chi2.cdf(LR_uc, df=1)

    return LR_uc, p_value

def christoffersen_test(violations_binary):
    """
    Christoffersen's independence test (LR_ind) and conditional coverage test (LR_cc)

    H0: VaR violations are independent (no clustering)

    Parameters:
    -----------
    violations_binary : array-like
        Binary sequence where 1 = violation, 0 = no violation

    Returns:
    --------
    LR_ind : float
        Independence test statistic
    p_value_ind : float
        P-value for independence test
    """
    violations = np.array(violations_binary)

    # Transition counts
    n00 = np.sum((violations[:-1] == 0) & (violations[1:] == 0))
    n01 = np.sum((violations[:-1] == 0) & (violations[1:] == 1))
    n10 = np.sum((violations[:-1] == 1) & (violations[1:] == 0))
    n11 = np.sum((violations[:-1] == 1) & (violations[1:] == 1))

    # Transition probabilities
    pi_0 = n01 / (n00 + n01) if (n00 + n01) > 0 else 0
    pi_1 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0
    pi = (n01 + n11) / len(violations)

    # Avoid log(0)
    if pi_0 == 0: pi_0 = 1e-10
    if pi_1 == 0: pi_1 = 1e-10
    if pi == 0: pi = 1e-10
    if 1 - pi_0 == 0: pi_0 = 1 - 1e-10
    if 1 - pi_1 == 0: pi_1 = 1 - 1e-10
    if 1 - pi == 0: pi = 1 - 1e-10

    # Independence test
    L1 = (1 - pi)**(n00 + n10) * pi**(n01 + n11)
    L2 = (1 - pi_0)**n00 * pi_0**n01 * (1 - pi_1)**n10 * pi_1**n11

    LR_ind = -2 * np.log(L1 / L2)
    p_value_ind = 1 - stats.chi2.cdf(LR_ind, df=1)

    return LR_ind, p_value_ind

def conditional_coverage_test(violations_binary, n, alpha=0.95):
    """
    Christoffersen's conditional coverage test (LR_cc = LR_uc + LR_ind)

    Tests both correct coverage AND independence

    Parameters:
    -----------
    violations_binary : array-like
        Binary sequence where 1 = violation, 0 = no violation
    n : int
        Total number of observations
    alpha : float
        VaR confidence level

    Returns:
    --------
    LR_cc : float
        Conditional coverage test statistic
    p_value_cc : float
        P-value from chi-squared distribution with 2 df
    """
    violations_count = np.sum(violations_binary)

    LR_uc, _ = kupiec_test(violations_count, n, alpha)
    LR_ind, _ = christoffersen_test(violations_binary)

    LR_cc = LR_uc + LR_ind
    p_value_cc = 1 - stats.chi2.cdf(LR_cc, df=2)

    return LR_cc, p_value_cc
