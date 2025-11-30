📌 논문 주제 정리 (Final Version)

Monte Carlo 및 Quasi-Monte Carlo 기반 VaR/CVaR 추정 및 백테스팅:
한국 주식·채권 포트폴리오를 대상으로 한 시뮬레이션 연구

1. 연구 배경 (Background)

금융기관은 시장 리스크 측정을 위해 Value at Risk(VaR) 및 **Conditional VaR(CVaR, Expected Shortfall)**을 핵심 지표로 활용한다.
한국 금융시장은 2020년 코로나 쇼크, 2022년 레고랜드 사태, 2023년 금리 급등기 등 급격한 변동성 구간과 구조적 충격을 여러 차례 경험했으며, 이러한 구간에서는 전통적인 리스크 평가 방식만으로는 정확한 tail-risk 포착이 어려워진다.

이에 따라 시나리오 기반 접근인 Monte Carlo(MC) VaR/CVaR이 널리 활용되나,
MC는 수렴 속도가 느리고, 많은 시나리오를 요구하며, tail 영역에서 오차가 커지는 문제가 존재한다.

반면 Quasi-Monte Carlo(QMC) 방식은 Sobol·Halton과 같은 저편차 시퀀스를 활용해
시뮬레이션의 효율성을 개선할 수 있어, 최근 금융공학 및 계산재무 분야에서 활발히 연구되고 있다.

본 논문은 이러한 흐름 속에서 MC 대비 QMC의 실질적 효율성, 분산 감소 효과, 그리고 한국 시장에서의 실증적 활용성을 검증하고자 한다.

2. 연구 목적 (Purpose)

본 연구의 목적은 다음과 같다:

Monte Carlo와 Quasi-Monte Carlo(Sobol/Halton) 기반 VaR/CVaR의
정확도·수렴 속도·계산 효율성을 정량적으로 비교한다.

**Variance Reduction 기법(Antithetic Variates, Control Variates)**을 적용하여
VaR/CVaR 추정 시 분산 감소 효과를 분석한다.

Control Variate는 **포트폴리오 기대수익률(μ)**을 통제변수로 사용한다.

한국 주식·채권 포트폴리오를 기반으로
**스트레스 구간(2020, 2022, 2023)**에서
MC/QMC 기반 VaR/CVaR 모델의 백테스트 결과 차이를 분석한다.

실무 관점에서
**“어떤 조건에서 QMC가 MC보다 우월한가”**에 대한
경계 조건(Boundary Condition) 및 실용적 가이드라인을 도출한다.

3. 연구 기여도 (Contribution)
3.1 계산적 기여 (Computational Contribution)

MC 대비 QMC의 수렴 특성, 오차 감소(RMSE), 시나리오 효율성, 계산 시간을 분석하여
난수 기반 시뮬레이션 알고리즘의 성능 비교라는 CS적 기여를 제공한다.

Antithetic Variates 및 Control Variates(μ 기반) 적용 시 분산 감소 효과를 정량화한다.

3.2 금융 실증 기여 (Financial Contribution)

변동성이 극단적으로 높았던 한국 금융시장 스트레스 구간에서
MC/QMC 기반 VaR 모델의 백테스트 실패율 차이를 분석한다.

MC와 QMC의 tail-risk 포착력 차이를 실증적으로 제시한다.

3.3 실무적 기여 (Practical Insight)

다음과 같은 실무 가이드라인을 제시하는 것을 목표로 한다:

어떤 자산 구조·변동성 수준·시나리오 규모에서 QMC 사용이 유리한가

Variance Reduction 적용 시 성능 향상 여부

한국형 스트레스 환경에서 어떤 모델이 더 안정적인가

4. 연구 질문 (Research Questions)
RQ1.

전통적 Monte Carlo와 Quasi-Monte Carlo(Sobol/Halton)는
VaR/CVaR 추정의 정확도와 수렴 속도에서 어떤 차이를 보이는가?

RQ2.

Variance Reduction 기법(Antithetic, Control Variates)은
VaR/CVaR 추정의 오차와 분산을 얼마나 감소시키는가?

RQ3.

QMC 기반 VaR/CVaR는
시뮬레이션 수가 증가할 때 MC보다 더 빠르게 수렴하는가?

RQ4. (강화된 버전)

2020 코로나 쇼크, 2022 레고랜드 사태, 2023 금리 급등기 등 한국 시장의 스트레스 구간에서
MC와 QMC 기반 VaR의 백테스트 실패율 차이는 통계적으로 유의미한가?

RQ5. (기여도 강화 핵심)

자산 차원, 변동성 수준, 시나리오 수 등 특정 조건에서 QMC의 우월성 또는 한계가 나타나는 경계 조건은 무엇인가?

5. 데이터 (Data)

주식: KOSPI200 ETF (예: TIGER 200)

채권: KTB 국채 ETF(3년/10년)

기간: 2018–2024

수익률 처리: 로그수익률, rolling covariance(20일/60일)

6. 방법론 (Methodology)
6.1 VaR/CVaR 추정 방식

Historical VaR

Parametric VaR(정규·t-분포 비교)

Monte Carlo VaR

Quasi-Monte Carlo VaR(Sobol, Halton)

CVaR(부가 분석; tail 평균 손실 비교 중심)

6.2 Variance Reduction

Antithetic Variates

Control Variates (통제변수: 포트폴리오 기대수익률 μ)

6.3 백테스팅

초과 횟수

Kupiec Test (LR_uc)

Christoffersen Test (LR_ind, LR_cc)

Stress period와 비교

7. 실험 구성 (Experiments)

MC vs QMC(Sobol·Halton)

VaR/CVaR 정확도 비교

오차(RMSE)

시뮬레이션 수 대비 수렴 속도

계산 시간

Variance Reduction 기법 적용 효과

MC vs MC+VR

QMC vs QMC+VR

분산 감소율

Stress 구간 실증 분석

코로나(2020)

레고랜드(2022)

금리 급등기(2023)

백테스트 성능 비교

MC vs QMC 초과횟수

LR 테스트

CVaR tail 비교(보조 분석)

경계 조건(Boundary Conditions) 도출

시나리오 수

자산 차원

변동성 수준

상관구조 변화

8. 예상 결과 (Expected Findings)

QMC가 MC 대비 더 빠른 수렴과 낮은 RMSE를 보임

VR 적용 시 오차 감소 효과 존재(특히 Antithetic)

스트레스 구간에서 QMC 기반 VaR의 백테스트 적합도 향상 기대

특정 조건(Dimension, N, Volatility 등)에서 QMC 우월성 또는 약점 도출
→ 실무 가이드라인으로 이어지는 “이 논문의 핵심 기여”

9. 논문 초안 목차 (Outline)

서론

이론적 배경

데이터 및 방법론

실증 분석

경계 조건 분석

논의

결론

부록