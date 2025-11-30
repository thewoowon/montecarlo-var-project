# Citation Status - 인용 작업 완료 현황

## ✅ 완료된 작업

### 한글 번역본 (Korean Translations)

#### PAPER_DRAFT_KO_Part1.md ✅
- [x] Basel Committee on Banking Supervision (2019) - Line 13
- [x] Jorion (2006) - Line 13
- [x] Glasserman (2003) - Line 13
- [x] Sobol (1967) - Line 15
- [x] Halton (1960) - Line 15
- [x] L'Ecuyer (2009) - Line 15

#### PAPER_DRAFT_KO_Part3.md ✅
- [x] Joe & Kuo (2008) - Direction numbers
- [x] Owen (1998) - Scrambling
- [x] Cody (1969) - Inverse normal approximation

#### PAPER_DRAFT_KO_Part6.md ✅
- [x] Glasserman (2003) - Antithetic Variates 설명
- [x] Glasserman et al. (1999) - Importance sampling

---

## ⏳ 영문 논문 (PAPER_DRAFT.md) - 수동 작업 필요

### Section 1: Introduction

#### Line 13 - 추가 필요
```
현재:
under Basel III framework.

수정 필요:
under Basel III framework (Basel Committee on Banking Supervision, 2019).
```

#### Line 13 - 추가 필요
```
현재:
and Monte Carlo (MC) simulation.

수정 필요:
and Monte Carlo (MC) simulation (Jorion, 2006).
```

#### Line 13 - 추가 필요
```
현재:
and high computational cost.

수정 필요:
and high computational cost (Glasserman, 2003).
```

#### Line 15 - 추가 필요
```
현재:
such as Sobol and Halton,

수정 필요:
such as Sobol (Sobol, 1967) and Halton (Halton, 1960),
```

#### Line 15 - 추가 필요
```
현재:
in financial applications.

수정 필요:
in financial applications (L'Ecuyer, 2009).
```

---

### Section 3: Methodology

#### Line 159 - 추가 필요
```
현재:
We use Joe-Kuo (2008) direction numbers,

수정 필요:
We use Joe-Kuo direction numbers (Joe & Kuo, 2008),
```

#### Line 187 - ✅ 이미 인용됨
```
Owen scrambling (Owen, 1998):
```

#### Line 277 - 추가 필요
```
현재:
using Cody's (1969) rational approximation,

수정 필요:
using Cody's rational approximation (Cody, 1969),
```

---

### Section 5: Discussion

#### Line 642 - ✅ 이미 인용됨
```
This finding aligns with Glasserman (2003), who notes...
```

#### Line 642 - ✅ 이미 인용됨
```
(Glasserman, Heidelberger, & Shahabuddin, 1999).
```

#### Line 655 - ✅ 이미 인용됨
```
**stratified sampling** (Owen, 1998) or **importance sampling** (Glasserman et al., 1999)
```

#### Line 683 - ✅ 이미 인용됨
```
(McNeil, Frey, & Embrechts, 2015),
```

---

## 📊 인용 통계

### 전체 참고문헌 수: 27개

#### 기초 이론 (Foundational Theory)
1. ✅ Boyle (1977) - Line 41
2. ✅ Boyle et al. (1997) - 참고문헌만
3. ⚠️ Caflisch (1998) - 참고문헌만 (본문 추가 권장)
4. ⚠️ Dick et al. (2013) - 참고문헌만 (본문 추가 권장)
5. ✅ Glasserman (2003) - Multiple locations
6. ⚠️ Halton (1960) - 추가 필요 (Line 15)
7. ⚠️ Kuo & Sloan (2005) - 참고문헌만 (Section 5.4 추가 권장)
8. ⚠️ L'Ecuyer (2009) - 추가 필요 (Line 15)
9. ✅ L'Ecuyer (2018) - 참고문헌만
10. ✅ L'Ecuyer & Lemieux (2002) - 참고문헌만
11. ✅ Lemieux (2009) - 참고문헌만
12. ✅ Morokoff & Caflisch (1995) - 참고문헌만
13. ✅ Niederreiter (1992) - 참고문헌만
14. ✅ Owen (1998) - Line 187, 655
15. ⚠️ Sobol (1967) - 추가 필요 (Line 15)

#### 분산 감소 (Variance Reduction)
16. ✅ Glasserman et al. (1999) - Line 642, 655
17. ✅ Nelson (1990) - 참고문헌만

#### VaR 및 리스크 관리 (VaR & Risk)
18. ⚠️ Basel Committee (2019) - 추가 필요 (Line 13)
19. ✅ Berkowitz & O'Brien (2002) - 참고문헌만
20. ✅ Campbell (2006) - 참고문헌만
21. ✅ Christoffersen (1998) - Line 49
22. ✅ Engle & Manganelli (2004) - 참고문헌만
23. ⚠️ Jorion (2006) - Line 41, 추가 필요 (Line 13)
24. ✅ Kupiec (1995) - Line 49
25. ✅ McNeil et al. (2015) - Line 683

#### 구현 관련 (Implementation)
26. ⚠️ Joe & Kuo (2008) - 추가 필요 (Line 159)
27. ⚠️ Cody (1969) - 추가 필요 (Line 277)

#### 한국 문헌 (Korean Sources)
28. ✅ 금융감독원 (2020) - 참고문헌만
29. ✅ 한국은행 (2023) - 참고문헌만

---

## 🎯 우선순위 작업

### 높음 (High Priority) - 본문에 반드시 추가 필요
1. **Basel Committee (2019)** - Line 13
2. **Jorion (2006)** - Line 13
3. **Glasserman (2003)** - Line 13
4. **Sobol (1967)** - Line 15
5. **Halton (1960)** - Line 15
6. **L'Ecuyer (2009)** - Line 15
7. **Joe & Kuo (2008)** - Line 159
8. **Cody (1969)** - Line 277

### 중간 (Medium Priority) - 본문 추가 권장
1. **Caflisch (1998)** - Section 4.1 수렴 속도 설명
2. **Dick et al. (2013)** - Section 3.7 복잡도 분석
3. **Kuo & Sloan (2005)** - Section 5.4 차원의 저주
4. **Berkowitz & O'Brien (2002)** - Section 4.4 백테스팅

---

## 📝 작업 방법

### 영문 논문 (PAPER_DRAFT.md)
1. CITATION_GUIDE.md 참조
2. 각 섹션별로 수동 수정
3. 텍스트 에디터에서 Find & Replace 활용

### 한글 번역본
- ✅ **이미 완료** (Part 1, 3, 6에 주요 인용 추가됨)

---

**최종 업데이트**: 2025-11-30
**완료율**: 한글 100% ✅ | 영문 60% ⚠️
