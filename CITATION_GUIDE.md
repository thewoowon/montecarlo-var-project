# Citation Guide for PAPER_DRAFT.md and Korean Translations

본 문서는 논문에 추가해야 할 인용(citation) 위치를 정리한 가이드입니다.

## 📚 Section 1: Introduction (서론)

### Line 13 - Basel III framework 언급
**현재**:
```
under Basel III framework.
```
**수정**:
```
under Basel III framework (Basel Committee on Banking Supervision, 2019).
```

### Line 13 - MC simulation 언급
**현재**:
```
and Monte Carlo (MC) simulation.
```
**수정**:
```
and Monte Carlo (MC) simulation (Jorion, 2006).
```

### Line 13 - 계산 비용 언급
**현재**:
```
and high computational cost.
```
**수정**:
```
and high computational cost (Glasserman, 2003).
```

### Line 15 - Sobol/Halton sequences
**현재**:
```
such as Sobol and Halton,
```
**수정**:
```
such as Sobol (Sobol, 1967) and Halton (Halton, 1960),
```

### Line 15 - QMC in finance
**현재**:
```
in financial applications.
```
**수정**:
```
in financial applications (L'Ecuyer, 2009).
```

---

## 📚 Section 2: Literature Review (문헌 연구)

### Line 41 - Boyle (1977) - 이미 인용됨 ✅
### Line 41 - Glasserman (2003) - 이미 인용됨 ✅
### Line 41 - Jorion (2006) - 이미 인용됨 ✅

### Line 45 - Sobol/Halton - 이미 인용됨 ✅
### Line 45 - L'Ecuyer (2009) - 이미 인용됨 ✅

### Line 49 - Kupiec/Christoffersen - 이미 인용됨 ✅

---

## 📚 Section 3: Methodology (방법론)

### Line 159 - Joe-Kuo direction numbers
**현재**:
```
**Direction Numbers**: We use Joe-Kuo (2008) direction numbers,
```
**수정**:
```
**Direction Numbers**: We use Joe-Kuo direction numbers (Joe & Kuo, 2008),
```

### Line 187 - Owen scrambling
**현재**:
```
To enable variance estimation while preserving low-discrepancy properties, we apply Owen scrambling (Owen, 1998):
```
**이미 인용됨 ✅**

### Line 277 - Cody approximation
**현재**:
```
`scipy.stats.norm.ppf` implements the inverse normal CDF (Φ^{-1}) using Cody's (1969) rational approximation,
```
**수정**:
```
`scipy.stats.norm.ppf` implements the inverse normal CDF (Φ^{-1}) using Cody's rational approximation (Cody, 1969),
```

---

## 📚 Section 4: Empirical Results (실증 결과)

### Line 335 - MC convergence rate 언급
**현재**:
```
MC RMSE decreases proportional to 1/n, while QMC exhibits faster 1/n rate,
```
**수정 (선택사항)**:
```
MC RMSE decreases proportional to 1/√n (Glasserman, 2003), while QMC exhibits faster 1/n rate (Caflisch, 1998),
```

---

## 📚 Section 5: Discussion (논의)

### Line 642 - Antithetic Variates failure
**현재**:
```
This finding aligns with Glasserman (2003), who notes that Antithetic Variates effectiveness
```
**이미 인용됨 ✅**

### Line 642 - Importance sampling
**현재**:
```
(Glasserman, Heidelberger, & Shahabuddin, 1999).
```
**이미 인용됨 ✅**

### Line 655 - Owen (1998) stratified sampling
**현재**:
```
**stratified sampling** (Owen, 1998) or **importance sampling** (Glasserman et al., 1999)
```
**이미 인용됨 ✅**

### Line 683 - McNeil et al. (2015) PCA dimension reduction
**현재**:
```
(McNeil, Frey, & Embrechts, 2015),
```
**이미 인용됨 ✅**

---

## 🔧 추가 권장 인용

### Computational Complexity (Section 3.7)
**Line 212 근처 - Asymptotic equivalence**:
```
**추가 추천**:
1. **Asymptotic Equivalence**: MC and QMC-Sobol share identical O(n·d² + n log n) complexity. QMC's superior accuracy (Section 4.1) stems from better constant factors and space-filling properties (Caflisch, 1998; Dick, Kuo, & Sloan, 2013), not asymptotic advantage.
```

### Curse of Dimensionality (Section 5.4)
**Line 671 근처**:
```
**추가 추천**:
The **658% efficiency gain for d=2 declining to 48% for d=15** confirms theoretical predictions about QMC's curse of dimensionality (Kuo & Sloan, 2005).
```

### Backtesting (Section 4.4)
**Line 409 근처**:
```
**추가 추천**:
**Christoffersen independence test fails** (p=0.000): Violations exhibit significant clustering, consistent with findings in Berkowitz & O'Brien (2002) for commercial bank VaR models.
```

### Korean Market Context
**새로 추가 가능**:
```
**섹션 5.3 또는 6에 추가**:
The extreme COVID-19 violations (22.58%) are consistent with global evidence of VaR model failures during the 2020 pandemic crisis, as documented by 한국은행 (2023) and 금융감독원 (2020).
```

---

## 📝 인용 형식 일관성 체크

### 이미 올바르게 인용된 부분 ✅
- Line 41: Boyle (1977), Glasserman (2003), Jorion (2006)
- Line 45: Sobol (1967), Halton (1960), L'Ecuyer (2009)
- Line 49: Kupiec (1995), Christoffersen (1998)
- Line 187: Owen (1998)
- Line 642: Glasserman (2003), Glasserman et al. (1999)
- Line 683: McNeil, Frey, & Embrechts (2015)

### 추가 필요한 부분 ⚠️
1. Basel III framework (line 13)
2. Joe-Kuo direction numbers (line 159)
3. Cody's approximation (line 277)
4. Theoretical convergence rates 설명 시 (선택사항)
5. Curse of dimensionality 이론 (선택사항)

---

## 🌏 한글 번역본 인용 처리

한글 논문에서는 **영문 인용을 그대로 유지**하되, 한국 문헌은 한글로 표기:

### 영문 저자 (그대로 유지)
```
Basel Committee on Banking Supervision (2019)
Glasserman (2003)
Owen (1998)
```

### 한국 문헌 (한글 표기)
```
금융감독원 (2020)
한국은행 (2023)
```

---

## ✅ 적용 방법

1. **영문 논문 (PAPER_DRAFT.md)**: 위의 수정사항 적용
2. **한글 번역본 (PAPER_DRAFT_KO_Part*.md)**: 동일한 위치에 동일한 인용 추가
   - Part 1 (서론): Basel, Jorion, Glasserman, Sobol, Halton, L'Ecuyer
   - Part 3 (방법론): Joe & Kuo, Cody
   - Part 4-6 (결과/논의): 이미 대부분 포함됨

---

**작성일**: 2025-11-30
**용도**: 논문 인용 추가 작업 가이드
