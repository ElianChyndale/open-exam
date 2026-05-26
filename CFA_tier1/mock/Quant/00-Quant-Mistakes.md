---
bucket: Quant
question_count: 12
---

# Quant Mock Mistakes

## Quantitative Methods | QM.Rates and Returns
- error_type: concept_confusion
- question_source: official_qbank
- source_type: screenshot
- wrong_choice_or_output: Selected A (Geometric mean return) and confused money-weighted return with time-weighted return / geometric mean.
- correct_resolution: For money-weighted return, build investor cash flows and solve IRR. Here the MWRR is about -2.22%, while TWRR is a separate measure and is positive at about 7.97%.
- evidence_refs: screenshot-session-2026-05-21
- evidence_assets: chat_image_1, chat_image_2
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | QM.Rates and Returns
- error_type: concept_confusion
- question_source: custom_drill
- source_type: typed
- wrong_choice_or_output: B. -10.32% (holding period return formula used instead of continuously compounded return)
- correct_resolution: r = ln(186.75/208.25) = ln(0.89676) = -0.10897 ≈ -10.90%. 连续复利收益率必须用 ln(P1/P0)，而非简单收益率 (P1-P0)/P0。
- evidence_refs: typed-q-2026-05-21-quant
- evidence_assets: 
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | QM.Rates and Returns
- error_type: concept_confusion
- question_source: custom_drill
- source_type: typed
- wrong_choice_or_output: B. the return earned by the manager prior to deduction of trading expenses.
- correct_resolution: C is correct. Gross return 已扣除交易费用（trading expenses 直接贡献于回报计算），但不含管理费/行政费。它是税前、非风险调整的，用于衡量经理投资能力。B 错在 gross return 实际已包含 trading expenses 的扣除（它们属于投资决策的一部分），而 A 错在 gross return 是税前且不调整风险。
- evidence_refs: typed-q-2026-05-21-quant-2
- evidence_assets: 
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | QM.Rates and Returns
- error_type: concept_confusion
- question_source: custom_drill
- source_type: typed
- wrong_choice_or_output: B. 3.98%. 错误路径：多减了 trading expenses 1.10%。即 (8.46%-1.10%-1.60%) 得 5.76% → 杠杆后 5.68% → 税后 3.98%
- correct_resolution: C. 5.00%。正确三步：(1) Net return = 8.46% - 1.60% = 6.86%（trading expenses已在gross return中，不重复减）(2) Leveraged return = 6.86% + (2500/7500)*(6.86%-6%) = 7.15% (3) After-tax = 7.15%*(1-0.30) = 5.00%
- evidence_refs: typed-q-2026-05-21-quant-3
- evidence_assets: 
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | unknown_from_screenshot
- error_type: concept_confusion
- question_source: unknown_from_screenshot
- source_type: screenshot
- wrong_choice_or_output: B. maturity premium
- correct_resolution: C. real risk-free interest rate. The real risk-free rate reflects the time preferences of individuals for current versus future real consumption.
- evidence_refs: chat-screenshot-2026-05-21-q38
- evidence_assets: chat_image_1
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | unknown_from_screenshot
- error_type: formula_misuse
- question_source: unknown_from_screenshot
- source_type: screenshot
- wrong_choice_or_output: 选择了 A. 1.42 percent。错误路径：在计算低于 target 的偏差时，没有把 target 2% 转成 0.02，导致 deviation 和 squared deviation 口径错误。
- correct_resolution: 若收益率按小数表示，则 target 2% 必须写成 0.02。低于 2% 的回报分别用 (0.015-0.02)^2、(-0.02-0.02)^2、(0-0.02)^2，合计 0.002025，再按题目口径开方得到 1.50%。核心不是公式变了，而是 percent 与 decimal 必须全程统一单位。
- evidence_refs: chat-screenshot-2026-05-25-target-semideviation
- evidence_assets: chat_image_1
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | unknown_from_user_note
- error_type: concept_confusion
- question_source: self_report
- source_type: typed
- wrong_choice_or_output: 把偏度图的 y 轴记成了别的含义，而不是 frequency（频率）。
- correct_resolution: 偏度图本质是在展示数据分布形状。y 轴表示 frequency（频率），x 轴表示变量取值或收益结果；判断左偏/右偏时先看尾巴方向，但读图前先锁定坐标轴含义。
- evidence_refs: chat-note-2026-05-25-skewness-axis
- evidence_assets: 
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | unknown_from_screenshot
- error_type: prompt_misread
- question_source: unknown_from_screenshot
- source_type: screenshot
- wrong_choice_or_output: 选择了 A. a less representative sample。错误路径不是知识点完全不会，而是疲劳下把题干方向看反了，把 "probability sampling compared to non-probability sampling" 误读成在求 non-probability sampling 的特征。
- correct_resolution: 正确答案是 C. a more representative sample。题干比较的是 probability sampling 相对于 non-probability sampling 的结果：probability sampling 给总体成员更均等的被抽中机会，因此通常更具代表性、更准确、更可靠。
- evidence_refs: chat-screenshot-2026-05-25-probability-sampling-misread
- evidence_assets: chat_image_1
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | unknown_from_screenshot
- error_type: concept_confusion
- question_source: unknown_from_screenshot
- source_type: screenshot
- wrong_choice_or_output: 选择了 A. random variable and the respective statistic。错误点在于把 sampling error 误记成样本内随机变量与统计量之间的差，而没有抓住它是 statistic 与被估计总体参数之间的差。
- correct_resolution: 正确答案是 C。Sampling error 指样本统计量（statistic）的观测值与它试图估计的总体参数/quantity 之间的差，而不是 random variable 与 statistic 之间的差。
- evidence_refs: chat-screenshot-2026-05-25-sampling-error-definition
- evidence_assets: chat_image_1
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | unknown_from_screenshot
- error_type: concept_confusion
- question_source: unknown_from_screenshot
- source_type: screenshot
- wrong_choice_or_output: 选择了 C. The standard deviation of the original sample。错误点在于把 bootstrap 下 sample mean 的 standard error，误解成依赖原始样本的标准差，而没有抓住它是由各次 resample 产生的均值分布来估计。
- correct_resolution: 正确答案是 A. The mean of each resample。Bootstrap 估计 sample mean 的 standard error，本质上是看所有 resamples 产生的 sample means 的离散程度，因此需要先得到每个 resample 的 mean；原始样本的 mean 或 standard deviation 都不是这个题目所需的直接输入。
- evidence_refs: chat-screenshot-2026-05-25-bootstrap-standard-error
- evidence_assets: chat_image_1
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | M08 Hypothesis Testing - nonparametric tests (exact LOS not shown)
- error_type: concept_confusion
- question_source: unknown
- source_type: screenshot
- wrong_choice_or_output: B. validity of the test depends on many assumptions.
- correct_resolution: A. data consist of ranked values. Nonparametric tests are most appropriate for ranked or ordinal data; they are used when parametric-test assumptions are not appropriate.
- evidence_refs: chat-2026-05-26-q18-nonparametric-test-screenshot
- evidence_assets: inline-chat-image:q18-nonparametric-test-2026-05-26
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md

## Quantitative Methods | M08 Hypothesis Testing - paired comparisons test (exact LOS not shown)
- error_type: formula_misuse
- question_source: unknown
- source_type: screenshot
- wrong_choice_or_output: C. accepted because the computed test statistic is less than 2.807.
- correct_resolution: A. rejected because the computed test statistic exceeds 2.807. For paired observations, use t = (mean difference - hypothesized difference) / (sample standard deviation of differences / sqrt(n)) = (4.25 - 0) / (6.25 / sqrt(25)) = 3.40. Since 3.40 > 2.807, reject H0.
- evidence_refs: chat-2026-05-26-q22-paired-comparisons-screenshot
- evidence_assets: inline-chat-image:q22-paired-comparisons-2026-05-26
- moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md