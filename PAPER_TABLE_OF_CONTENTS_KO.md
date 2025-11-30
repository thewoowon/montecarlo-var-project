# 논문 차례 (국문)

## VaR 추정을 위한 몬테카를로 및 준몬테카를로 방법의 알고리즘적 비교: 복잡도 분석과 한국 금융시장 실증 연구

---

## 초록 (Abstract)

## 키워드 (Keywords)
Value at Risk, Quasi-Monte Carlo, Risk Management, Backtesting, Korean Financial Markets

---

## 1. 서론 (Introduction)

### 1.1 연구 목적 (Research Objectives)
1. MC 대 QMC (Sobol/Halton)의 수렴 특성 비교
2. Antithetic Variates 및 Control Variates 기법의 분산 감소 효과 정량화
3. 한국 시장 스트레스 기간 동안 백테스팅 성능 평가 및 통계적 유의성 검정
4. QMC가 우수하거나 열등한 경계 조건 식별
5. 리스크 관리자를 위한 실용적 가이드라인 제공

### 1.2 기여도 (Contributions)
- **계산적 기여**: 알고리즘 수준 분석
- **금융적 기여**: 한국 시장 위기 기간 실증 연구
- **실용적 기여**: 경계 조건 분석 및 의사결정 규칙

---

## 2. 문헌 연구 (Literature Review)

### 2.1 금융 분야의 몬테카를로 방법 (Monte Carlo Methods in Finance)

### 2.2 준몬테카를로 방법 (Quasi-Monte Carlo Methods)

### 2.3 VaR 백테스팅 (VaR Backtesting)

### 2.4 연구 격차 (Research Gap)

---

## 3. 방법론 (Methodology)

### 3.1 데이터 (Data)
- 자산: KOSPI 200 ETF, KTB 3년물 ETF, KTB 10년물 ETF
- 표본 기간: 2018-01-01 ~ 2024-12-30 (1,690일)
- 스트레스 기간: COVID-19 (2020.02-04), Legoland (2022.09-12), 금리급등 (2023.01-06)

### 3.2 VaR 및 CVaR 추정 (VaR and CVaR Estimation)

### 3.3 시뮬레이션 방법 (Simulation Methods)
- 몬테카를로 (MC)
- 준몬테카를로 (QMC): Sobol, Halton

### 3.4 분산 감소 기법 (Variance Reduction Techniques)
- Antithetic Variates
- Control Variates

### 3.5 백테스팅 프레임워크 (Backtesting Framework)
- Kupiec Test (무조건부 커버리지)
- Christoffersen Test (독립성)
- 조건부 커버리지 검정

### 3.6 저불일치 수열 구현 (Low-Discrepancy Sequence Implementation)
- Sobol 수열 생성
  - Direction Numbers (Joe-Kuo 2008)
  - Gray Code 최적화
- Halton 수열 생성
  - van der Corput 수열
  - 고차원 상관성 문제
- Scrambling: Owen vs Digital Shift

### 3.7 계산 복잡도 분석 (Computational Complexity Analysis)
- 시간 복잡도 (Time Complexity)
- 메모리 복잡도 (Memory Complexity)
- 실증 검증 (Empirical Validation)

### 3.8 구현 세부사항 (Implementation Details)
- 소프트웨어 환경 (Python 3.11.4, NumPy, SciPy, Pandas)
- 하드웨어 (Apple M2 Pro)
- 재현성 (Reproducibility)
- 코드 및 데이터 가용성

### 3.9 통계적 유의성 검정 (Statistical Significance Testing)
- Bootstrap 신뢰구간
- McNemar Test

---

## 4. 실증 결과 (Empirical Results)

### 4.1 수렴 분석 (Convergence Analysis)
- **표 1**: 시뮬레이션 횟수별 VaR 추정 정확도
- **표 2**: CVaR 추정 비교 (n=10,000)

### 4.2 분산 감소 분석 (Variance Reduction Analysis)
- **표 3**: 분산 감소 기법 효과

### 4.3 통계적 유의성 검정 (Statistical Significance Testing)
- **표 4**: Bootstrap 신뢰구간 (n=10,000, 100회 반복)

### 4.4 백테스팅 성능 (Backtesting Performance)
- **표 5**: 전체 기간 백테스팅 결과 (n=1,438일)
- **표 6**: 스트레스 기간 위반율

#### 4.4.1 위반 군집 분석 (Violation Clustering Analysis)
- 군집 통계량
- 전이 행렬
- 주요 위반 군집
- **그림 5**: 위반 타임라인 (christoffersen_clustering.png)

### 4.5 McNemar 검정 결과 (McNemar Test Results)
- **표 7**: 쌍대 위반 비교

### 4.6 경계 조건 분석 (Boundary Condition Analysis)
- **표 8**: 자산 차원별 QMC 효율성 이득 (d=2~50)
- **표 9**: 시장 조건별 QMC 성능
- 실용적 가이드라인

### 4.7 강건성 검증 (Robustness Checks)

#### 4.7.1 5-자산 포트폴리오 일반화 (5-Asset Portfolio Generalization)
- **표 10**: 5-자산 포트폴리오 결과 (n=10,000, 100회)

#### 4.7.2 다변량 t-분포 검정 (Multivariate t-Distribution Test)
- **표 11**: t-분포 강건성 (n=10,000, 100회)

---

## 5. 논의 (Discussion)

### 5.1 계산 효율성 대 백테스팅 성능 (Computational Efficiency vs Backtesting Performance)

### 5.2 분산 감소 우위 (Variance Reduction Dominance)
- Antithetic Variates 실패 메커니즘
- 실증 증거
- 실용적 함의

### 5.3 한국 시장 스트레스 동학 (Korean Market Stress Dynamics)
- COVID-19 (22.58% 위반)
- Legoland (9.76% 위반)
- 금리 급등 2023 (0.83% 위반)

### 5.4 경계 조건 및 차원의 저주 (Boundary Conditions and Curse of Dimensionality)

### 5.5 한계 (Limitations)
- 표본 기간
- 포트폴리오 단순성 (방법론적 선택)
- 일반화 증거
- 분포 가정
- 백테스팅 기간
- 계산 환경 및 병렬화
  - MC: Embarrassingly Parallel
  - QMC: Sequential Dependency
  - Production Trade-off

---

## 6. 결론 (Conclusion)

### 주요 발견사항 (Key Findings)
1. QMC는 동일 시뮬레이션 횟수에서 MC 대비 2.7-6.2배 낮은 RMSE 달성
2. 백테스팅 성능에서 통계적으로 유의한 차이 없음 (McNemar test p=1.000)
3. Control Variate 기법이 분산 감소 우위 (99.99%)
4. QMC 효율성 이득은 차원 의존적 (d=2: +658% → d=15: +48%)
5. 한국 시장 스트레스 기간에 모델 한계 드러남 (COVID-19: 22.58% 위반율)
6. 포트폴리오 구조 및 분포에 걸쳐 강건성 검증 (5-자산: +117%, t(ν=5): +192%)

### 실용적 권장사항 (Practical Recommendations)
- d≤10, n≥5,000인 포트폴리오에 QMC-Sobol 사용
- 시뮬레이션 방법과 무관하게 Control Variates 구현
- 스트레스 테스팅 및 시나리오 분석으로 VaR 보완
- 위반 군집 모니터링 (Christoffersen test)

### 향후 연구 (Future Research)
- Copula 기반 모델 확장
- GARCH 기반 동적 시뮬레이션
- 경로 의존성 있는 파생상품 포트폴리오
- 고빈도 일중 VaR
- 국가 간 비교 (한국, 미국, 유럽)
- 기계학습 기반 적응형 QMC 수열 선택

---

## 참고문헌 (References)

### 기초 Monte Carlo & QMC 이론
- Boyle (1977), Glasserman (2003), Sobol (1967), Halton (1960)
- L'Ecuyer (2009), Owen (1998), Joe & Kuo (2008)

### 분산 감소 기법
- Glasserman et al. (1999), Nelson (1990)

### VaR 및 리스크 관리
- Kupiec (1995), Christoffersen (1998), Jorion (2006)
- McNeil, Frey, & Embrechts (2015)
- Basel Committee (2019)
- 금융감독원 (2020), 한국은행 (2023)

### 구현 관련
- Cody (1969): Inverse normal CDF

---

## 부록

**총 단어 수**: ~6,684 단어
**그림**: 5개 (수렴, 분산 감소, 스트레스 백테스팅, 경계 조건, bootstrap CI, 위반 클러스터링)
**표**: 14개 (본문) + 추가 (부록)

---

## 핵심 용어 정리 (Key Terms)

| 영문 | 국문 | 설명 |
|------|------|------|
| Monte Carlo (MC) | 몬테카를로 | 의사난수 기반 시뮬레이션 |
| Quasi-Monte Carlo (QMC) | 준몬테카를로 | 저불일치 수열 기반 시뮬레이션 |
| Value at Risk (VaR) | 위험가치 | 95% 신뢰수준 손실 분위수 |
| Conditional VaR (CVaR) | 조건부 위험가치 | VaR 초과 기대손실 |
| Sobol Sequence | Sobol 수열 | 저불일치 수열 (direction numbers) |
| Halton Sequence | Halton 수열 | 소수 기반 저불일치 수열 |
| Gray Code Optimization | Gray Code 최적화 | O(m)→O(1) 복잡도 개선 |
| Owen Scrambling | Owen Scrambling | 중첩 무작위 순열 |
| Antithetic Variates | Antithetic Variates | 대칭 쌍 표본 (+Z, -Z) |
| Control Variates | Control Variates | 기댓값 알려진 변수로 조정 |
| Kupiec Test | Kupiec 검정 | 무조건부 커버리지 검정 |
| Christoffersen Test | Christoffersen 검정 | 독립성 검정 |
| McNemar Test | McNemar 검정 | 쌍대 비교 검정 |
| Bootstrap CI | Bootstrap 신뢰구간 | 재표본 기반 구간 추정 |
| Curse of Dimensionality | 차원의 저주 | 고차원에서 QMC 효율 저하 |
| RMSE | 평균제곱근오차 | Root Mean Squared Error |
| Complexity Analysis | 복잡도 분석 | 시간/메모리 복잡도 |

---

**작성일**: 2024-11-29
**상태**: ✅ 최종 확정
**용도**: 논문 제출, 발표자료, 심사위원 참고
