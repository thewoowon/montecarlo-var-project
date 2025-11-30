**Time Complexity**

Table below summarizes asymptotic and practical complexity for n simulations in d dimensions:

| Operation | MC | QMC-Sobol | QMC-Halton |
|-----------|-----|-----------|------------|
| Random number generation | O(n·d) | O(n·d) [Gray code] | O(n·d·log p_d) |
| Inverse normal CDF | O(n·d) | O(n·d) | O(n·d) |
| Cholesky decomposition | O(d³) [once] | O(d³) [once] | O(d³) [once] |
| Matrix-vector products | O(n·d²) | O(n·d²) | O(n·d²) |
| Sorting for VaR quantile | O(n log n) | O(n log n) | O(n log n) |
| **Total** | **O(n·d² + n log n)** | **O(n·d² + n log n)** | **O(n·d² + n·d·log p_d)** |

**Memory Complexity**

| Component | MC | QMC-Sobol | QMC-Halton |
|-----------|-----|-----------|------------|
| Simulation array | O(n·d) | O(n·d) | O(n·d) |
| Direction numbers | — | O(d·m) [m≈32] | — |
| Working buffers | O(d²) | O(d²) | O(d²) |
| **Total** | **O(n·d)** | **O(n·d + 32d)** | **O(n·d)** |

**McNemar Test**:
Paired test comparing MC and QMC violation indicators on same dates:

| | QMC Violation | QMC No Violation |
|---|---|---|
| **MC Violation** | n_11 | n_10 |
| **MC No Violation** | n_01 | n_00 |

**Table 1**: VaR Estimation Accuracy by Simulation Count

| Simulations | MC RMSE | QMC-Sobol RMSE | QMC-Halton RMSE | Sobol Speedup |
|-------------|---------|----------------|-----------------|---------------|
| 100 | 0.000967 | 0.000528 | 0.000425 | 1.8× |
| 500 | 0.000428 | 0.000152 | 0.000201 | 2.8× |
| 1,000 | 0.000310 | 0.000119 | 0.000092 | 2.6× |
| 2,000 | 0.000213 | 0.000068 | 0.000068 | 3.1× |
| 5,000 | 0.000129 | 0.000028 | 0.000045 | 4.6× |
| **10,000** | **0.000074** | **0.000027** | **0.000024** | **2.7×** |
| 20,000 | 0.000080 | 0.000013 | 0.000016 | **6.2×** |

**Table 2**: CVaR Estimation Comparison (n=10,000)

| Method | CVaR Mean | CVaR RMSE | Time (sec) |
|--------|-----------|-----------|------------|
| MC | -0.009248 | 0.000101 | 0.00145 |
| QMC-Sobol | -0.009232 | 0.000010 | 0.00128 |
| QMC-Halton | -0.009231 | 0.000013 | 0.00404 |

**Table 3**: Variance Reduction Technique Effectiveness

| Method | VaR Std Dev | Variance Reduction vs MC |
|--------|-------------|--------------------------|
| MC (baseline) | 0.0000868 |  |
| MC + Antithetic | 0.0000904 | -4.2% |
| **MC + Control Variate** | **0.0000000** | **99.99%** |
| QMC-Sobol | 0.0000257 | **70.4%** |
| QMC-Sobol + Antithetic | 0.0000261 | 69.9% |
| **QMC-Sobol + Control Variate** | **0.0000000** | **99.997%** |

**Table 4**: Bootstrap Confidence Intervals (n=10,000, 100 iterations)

| Method | VaR Mean | 95% CI Lower | 95% CI Upper | CI Width |
|--------|----------|--------------|--------------|----------|
| MC | -0.007346 | -0.007524 | -0.007149 | 0.000375 |
| QMC-Sobol | -0.007340 | -0.007385 | -0.007297 | 0.000088 |
| QMC-Halton | -0.007348 | -0.007392 | -0.007306 | 0.000086 |

**Table 5**: Full Period Backtesting Results (n=1,438 days)

| Method | Violations | Violation Rate | Expected | Kupiec LR | Kupiec p-value | Christ. LR | Christ. p-value | LR_cc | p-value (cc) |
|--------|------------|----------------|----------|-----------|----------------|------------|-----------------|-------|--------------|
| MC | 72 | 5.01% | 5.00% | 0.000 | 0.990 | 14.264 | 0.000 | 14.264 | 0.001 |
| QMC-Sobol | 72 | 5.01% | 5.00% | 0.000 | 0.990 | 14.264 | 0.000 | 14.264 | 0.001 |
| QMC-Halton | 72 | 5.01% | 5.00% | 0.000 | 0.990 | 14.264 | 0.000 | 14.264 | 0.001 |

**Table 6**: Stress Period Violation Rates

| Period | Sample Size | MC Violations | MC Rate | Expected | Excess Violations |
|--------|-------------|---------------|---------|----------|-------------------|
| **COVID-19 Crash** | 62 | 14 | **22.58%** | 5.00% | **+17.58%** |
| **Legoland Crisis** | 82 | 8 | **9.76%** | 5.00% | **+4.76%** |
| **Rate Surge 2023** | 121 | 1 | **0.83%** | 5.00% | **-4.17%** |
| Full Period (2020-2024) | 1,205 | 65 | 5.39% | 5.00% | +0.39% |

**Table 7**: Paired Violation Comparison

| Comparison | Both Fail | Only Method 1 | Only Method 2 | Both Pass | ǲ | p-value | Significant? |
|------------|-----------|---------------|---------------|-----------|-----|---------|--------------|
| MC vs QMC-Sobol | 72 | 0 | 0 | 1,366 | 0.000 | 1.000 | No |
| MC vs QMC-Halton | 72 | 0 | 0 | 1,366 | 0.000 | 1.000 | No |

**Table 8**: QMC Efficiency Gain by Asset Dimension

| Dimension (d) | MC Std | QMC-Sobol Std | Efficiency Gain |
|---------------|--------|---------------|-----------------|
| 2 | 0.000133 | 0.000018 | **+658%** |
| 3 | 0.000097 | 0.000023 | **+315%** |
| 5 | 0.000097 | 0.000054 | +80% |
| 10 | 0.000091 | 0.000052 | +76% |
| 15 | 0.000075 | 0.000050 | +48% |
| **20** | **0.000289** | **0.000172** | **+68%** |
| **30** | **0.000510** | **0.000286** | **+79%** |
| **50** | **0.000438** | **0.000296** | **+48%** |

**Table 9**: QMC Performance Across Market Conditions

| Condition | Factor | MC Std | QMC Std | Efficiency Gain |
|-----------|--------|--------|---------|-----------------|
| **Volatility** | 0.5� | 0.000067 | 0.000019 | +254% |
| | 1.0� | 0.000097 | 0.000022 | +347% |
| | 2.0� | 0.000130 | 0.000034 | +282% |
| | 3.0� | 0.000163 | 0.000039 | +316% |
| **Correlation** | 0.1 | 0.000088 | 0.000021 | +321% |
| | 0.5 | 0.000119 | 0.000020 | +486% |
| | 0.9 | 0.000120 | 0.000025 | +383% |

**Practical Guidelines** (RQ5 Summary):

| Condition | Recommendation | Expected Benefit |
|-----------|---------------|------------------|
| d ≤ 3, n ≥ 5,000 | **Use QMC-Sobol** | 3-7× RMSE reduction |
| 3 < d ≤ 10, n ≥ 10,000 | **Use QMC-Sobol** | 1.5-2× RMSE reduction |
| d > 15 | **Use MC or QMC** | Minimal difference |
| High volatility regime | **Use QMC-Sobol** | Robust 3× gain |
| Need Control Variate | **Implement regardless** | 99%+ variance reduction |
| Real-time systems | **QMC with n=5,000** | Fast + accurate |

**Table 10**: 5-Asset Portfolio Results (n=10,000, 100 runs)

| Method | VaR RMSE | VaR Std | Efficiency Gain | Backtest Violations |
|--------|----------|---------|-----------------|---------------------|
| MC | 0.000078 | 0.000068 | - | 84 (5.85%) |
| QMC-Sobol | 0.000036 | 0.000024 | **+117.5%** | 83 (5.78%) |
| QMC-Halton | 0.000038 | 0.000027 | **+107.5%** | 83 (5.78%) |

**Table 11**: t-Distribution Robustness (n=10,000, 100 runs)

| Distribution | Method | VaR RMSE | Efficiency Gain | Reference VaR |
|--------------|--------|----------|-----------------|---------------|
| **t(ν=5)** | MC | 0.000115 | - | -0.007058 |
| | QMC-Sobol | 0.000039 | **+192.4%** | |
| | QMC-Halton | 0.000039 | **+197.8%** | |
| **t(ν=7)** | MC | 0.000117 | - | -0.007233 |
| | QMC-Sobol | 0.000054 | **+115.6%** | |
| | QMC-Halton | 0.000062 | **+88.6%** | |
| **Normal** | MC | 0.000074 | - | -0.007346 |
| (baseline) | QMC-Sobol | 0.000027 | **+174.1%** | |