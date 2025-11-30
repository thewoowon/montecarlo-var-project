## 6. 결론

본 연구는 다수의 스트레스 기간에 걸친 한국 금융시장 데이터를 사용하여 VaR 및 CVaR 추정을 위한 몬테카를로 대 준몬테카를로 방법에 대한 포괄적인 실증 증거를 제공한다. 주요 발견사항은 다음과 같다:

1. **QMC는 동등한 시뮬레이션 횟수에서 MC보다 2.7-6.2배 낮은 RMSE를 달성**하며, 더 큰 표본(n≥5,000)에서 이점이 증가

2. 계산 효율성 차이에도 불구하고 백테스팅 성능에서 **통계적으로 유의한 차이 없음** (McNemar 검정 p=1.000)

3. **Control Variate 기법이 분산 감소를 지배** (99.99%), QMC 단독(70.4%) 또는 Antithetic Variates (-4.2%)를 훨씬 초과

4. **QMC 효율성 이득은 차원 의존적**: d=2에서 658% 이득, d=15에서 48%로 감소하여 실용적 구현을 위한 실증 가이드 제공

5. **한국 시장 스트레스 기간은 모델 한계를 드러냄**: COVID-19 붕괴 동안 22.58% 위반율은 극단적 사건 동안 VaR 과소평가를 나타내며, 시뮬레이션 방법 선택과 무관

6. **포트폴리오 구조와 분포에 걸쳐 강건성 검증**: QMC 이점이 5-자산 포트폴리오(+117% 효율성) 및 ν=5의 다변량 Student-t 분포(+192% 효율성)에서 지속되어 3-자산 정규분포 기준을 넘어선 일반화 가능성 확인

**실용적 권장사항**:

- d≤10 및 n≥5,000 시나리오를 갖는 포트폴리오에 계산 효율성을 극대화하기 위해 **QMC-Sobol 사용**
- 시뮬레이션 방법과 무관하게 포트폴리오 기대수익률을 사용하여 **Control Variates 구현**
- 특히 신흥시장 노출에 대해 **스트레스 테스팅 및 시나리오 분석으로 VaR 보완**
- 변동성 체제 전환 동안 모델 부적절성을 감지하기 위해 **위반 군집화 모니터링** (Christoffersen 검정)

**향후 연구**:

copula 기반 모델, GARCH 기반 동적 시뮬레이션, 경로 의존성을 갖는 파생상품 포트폴리오, 고빈도 일중 VaR로의 확장은 QMC 적용 가능성을 추가로 검증할 것이다. 국가 간 비교(한국, 미국, 유럽 시장)는 관찰된 패턴이 시장 특정인지 보편적인지 밝힐 수 있다. 마지막으로, 기계학습 기반 적응형 QMC 수열 선택은 현재 테스트된 d≤15 범위를 넘어 고차원 성능을 잠재적으로 개선할 수 있다.

본 연구는 위험가치 추정을 위해 QMC 방법이 표준 몬테카를로 대비 이점을 제공하는 시기, 장소, 이유를 엄밀하게 정량화함으로써 계산 금융에 대한 학술 문헌과 실무적 리스크 관리 모두에 기여한다.

---

## 참고문헌

### 기초 Monte Carlo & QMC 이론

Boyle, P. P. (1977). Options: A Monte Carlo approach. *Journal of Financial Economics*, 4(3), 323-338.

Boyle, P., Broadie, M., & Glasserman, P. (1997). Monte Carlo methods for security pricing. *Journal of Economic Dynamics and Control*, 21(8-9), 1267-1321.

Caflisch, R. E. (1998). Monte Carlo and quasi-Monte Carlo methods. *Acta Numerica*, 7, 1-49.

Dick, J., Kuo, F. Y., & Sloan, I. H. (2013). High-dimensional integration: The quasi-Monte Carlo way. *Acta Numerica*, 22, 133-288.

Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer.

Halton, J. H. (1960). On the efficiency of certain quasi-random sequences of points in evaluating multi-dimensional integrals. *Numerische Mathematik*, 2(1), 84-90.

Kuo, F. Y., & Sloan, I. H. (2005). Lifting the curse of dimensionality. *Notices of the AMS*, 52(11), 1320-1328.

L'Ecuyer, P. (2009). Quasi-Monte Carlo methods with applications in finance. *Finance and Stochastics*, 13(3), 307-349.

L'Ecuyer, P. (2018). Randomized quasi-Monte Carlo: An introduction for practitioners. In *Monte Carlo and Quasi-Monte Carlo Methods* (pp. 29-52). Springer.

L'Ecuyer, P., & Lemieux, C. (2002). Recent advances in randomized quasi-Monte Carlo methods. *Modeling Uncertainty: An Examination of Stochastic Theory, Methods, and Applications*, 419-474.

Lemieux, C. (2009). *Monte Carlo and Quasi-Monte Carlo Sampling*. Springer.

Morokoff, W. J., & Caflisch, R. E. (1995). Quasi-Monte Carlo integration. *Journal of Computational Physics*, 122(2), 218-230.

Niederreiter, H. (1992). *Random Number Generation and Quasi-Monte Carlo Methods*. SIAM.

Owen, A. B. (1998). Scrambling Sobol' and Niederreiter-Xing points. *Journal of Complexity*, 14(4), 466-489.

Sobol, I. M. (1967). On the distribution of points in a cube and the approximate evaluation of integrals. *USSR Computational Mathematics and Mathematical Physics*, 7(4), 86-112.

### 분산 감소 기법

Glasserman, P., Heidelberger, P., & Shahabuddin, P. (1999). Asymptotically optimal importance sampling and stratification for pricing path-dependent options. *Mathematical Finance*, 9(2), 117-152.

Nelson, B. L. (1990). Control variate remedies. *Operations Research*, 38(6), 974-992.

### VaR 및 리스크 관리

Basel Committee on Banking Supervision. (2019). *Minimum Capital Requirements for Market Risk*. Bank for International Settlements.

Berkowitz, J., & O'Brien, J. (2002). How accurate are value-at-risk models at commercial banks? *Journal of Finance*, 57(3), 1093-1111.

Campbell, S. D. (2006). A review of backtesting and backtesting procedures. *Journal of Risk*, 9(2), 1-17.

Christoffersen, P. F. (1998). Evaluating interval forecasts. *International Economic Review*, 39(4), 841-862.

Engle, R. F., & Manganelli, S. (2004). CAViaR: Conditional autoregressive value at risk by regression quantiles. *Journal of Business & Economic Statistics*, 22(4), 367-381.

Jorion, P. (2006). *Value at Risk: The New Benchmark for Managing Financial Risk* (3rd ed.). McGraw-Hill.

Kupiec, P. H. (1995). Techniques for verifying the accuracy of risk measurement models. *Journal of Derivatives*, 3(2), 73-84.

McNeil, A. J., Frey, R., & Embrechts, P. (2015). *Quantitative Risk Management: Concepts, Techniques and Tools* (Revised Edition). Princeton University Press.

금융감독원. (2020). 금융회사 리스크관리 모범규준.

한국은행. (2023). 금융안정보고서.

### 구현 관련

Joe, S., & Kuo, F. Y. (2008). Constructing Sobol sequences with better two-dimensional projections. *SIAM Journal on Scientific Computing*, 30(5), 2635-2654.

Cody, W. J. (1969). Rational Chebyshev approximations for the error function. *Mathematics of Computation*, 23(107), 631-637.

---

**총 단어 수**: ~6,684 단어
**그림**: 5개 (수렴, 분산 감소, 스트레스 백테스팅, 경계 조건, bootstrap CI)
**표**: 14개 (본문) + 추가 (부록)

---

*교신저자*: [귀하의 이름]
*소속*: [귀하의 기관]
*이메일*: [귀하의 이메일]
*사사*: 귀중한 피드백을 제공해주신 [지도교수/동료]께 감사드립니다.

---

**논문 초안 완료**

---

**파일**: PAPER_DRAFT_KO_Part7.md (결론 Section 6 + 참고문헌)
**상태**: ✅ 완료
**전체 번역**: ✅ **완료**
