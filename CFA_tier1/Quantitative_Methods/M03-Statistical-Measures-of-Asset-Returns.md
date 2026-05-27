---
title: "M03: Statistical Measures of Asset Returns"
description: "CFA Level I 2026 Quantitative Methods 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "Quantitative Methods"
topic_area: "Quantitative_Methods"
level: "CFA Level I"
exam_year: 2026
exam_weight: "6-9%"
module: "M03"
official_module: "Module 3: Statistical Measures of Asset Returns"
los_count: 4
difficulty: "计算+解释"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - Quantitative_Methods
---

# M03: Statistical Measures of Asset Returns

## 0. Reading Contract 学习契约

- **Official module**: Module 3: Statistical Measures of Asset Returns.
- **Official pages**: Learning Outcomes; 3.01 Introduction; 3.02 Measures of Central Tendency and Location; 3.03 Measures of Dispersion; 3.04 Measures of Shape of a Distribution; 3.05 Correlation between Two Variables.
- **LOS contract**: calculate, interpret, and evaluate central tendency, location, dispersion; interpret and evaluate skewness/kurtosis; interpret correlation.
- **Evidence rule**: record whether the miss was formula selection, sample/population denominator, outlier/shape interpretation, or correlation language.

## 1. Module Brief 模块定位

M03 describes a return distribution before any formal inference. 中文上它回答“这个收益分布的中心在哪里、散得多远、尾巴长在哪边、两变量是否线性联动”。

## 2. Curriculum Spine 教材正文主线

1. **Measures of Central Tendency and Location**: arithmetic mean, sample mean, median, mode, quantiles, and outlier handling.
2. **Measures of Dispersion**: range, MAD, variance, standard deviation, downside deviation, coefficient of variation.
3. **Measures of Shape**: skewness tells tail direction; kurtosis tells tail thickness.
4. **Correlation between Two Variables**: covariance/correlation describe linear co-movement, with properties and limitations.

## 3. Exam Translation 考试翻译

| Prompt trigger | Exam action | Output language |
|---|---|---|
| typical value with outliers | prefer median | "Median is more robust to extreme observations." |
| single-period expected return | use arithmetic mean | "Arithmetic mean estimates one-period average." |
| compound annual growth | use geometric mean | "Geometric mean measures compounded growth." |
| average valuation multiple | use harmonic mean | "Harmonic mean is suitable for ratios." |
| sample variance | divide by `n-1` | "Sample variance uses degrees-of-freedom correction." |
| negative skew / fat tails | interpret downside and tail risk | "Negative skew and high kurtosis increase extreme loss concern." |
| high correlation | state association, not causality | "Correlation measures linear association only." |

## 4. Formula & Decision Bench 公式与决策台

| Formula / framework | Use | Trap check |
|---|---|---|
| `mu=sum(x_i)/N`; `xbar=sum(x_i)/n` | population/sample mean | Identify population vs sample. |
| `GM=[prod(1+R_i)]^(1/n)-1` | compound return | All returns must be in gross form before multiplying. |
| `HM=n/sum(1/x_i)` | average ratios | Inputs cannot be zero or negative in normal ratio use. |
| `L_p=(n+1)p/100` | percentile location | Interpolate if location is non-integer. |
| `sigma^2=sum(x_i-mu)^2/N` | population variance | Population denominator is N. |
| `s^2=sum(x_i-xbar)^2/(n-1)` | sample variance | Sample denominator is `n-1`. |
| `CV=s/xbar` | relative dispersion | Unstable when mean is near zero. |
| `Skewness=E[(X-mu)^3]/sigma^3` | asymmetry | Long tail direction sets sign. |
| `Excess kurtosis=kurtosis-3` | tail thickness vs normal | Fat tails are kurtosis, not skewness. |
| `rho=Cov(X,Y)/(sigma_X sigma_Y)` | correlation | Unitless linear association in `[-1,+1]`. |

## 5. Practice & Mock Evidence 题库证据

- Official textbook index marks practice and solutions as available.
- Evidence tags: `sample_denominator`, `mean_choice`, `outlier`, `skew_kurtosis`, `correlation_interpretation`, `cv`.
- In future mistake records, preserve the dataset and whether the question says sample, population, typical, compound, or relative risk.

## 6. Trap Ledger 陷阱账本

| Trap | Correct rule |
|---|---|
| Sample variance divided by n | Use `n-1`. |
| Arithmetic mean used for compound growth | Use geometric mean. |
| Fat tails called skewness | Fat tails are kurtosis; skewness is asymmetry. |
| Correlation interpreted as causation | Correlation only describes linear association. |
| CV used when mean is close to zero | CV may be misleading. |

## 7. Final Recall Sheet 最后回忆页

- Mean is sensitive to outliers; median is robust.
- `AM >= GM >= HM` for positive data where all are defined.
- Sample variance uses `n-1`.
- Negative skew means left tail; high kurtosis means more tail events.
- Correlation sign = direction; magnitude = linear strength; never equals causality.
