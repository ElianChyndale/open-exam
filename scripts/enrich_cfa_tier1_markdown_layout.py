"""Enrich CFA Level I 2026 Markdown notes with stable study layouts.

The script treats the official registry as immutable source metadata and rewrites
the projection-layer Markdown files in CFA_tier1/. It also records how legacy
notes were mapped into official 2026 modules so future enrichment can be audited.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / ".system" / "memory" / "strategy" / "cfa-2026-official-module-registry.json"
LEGACY_MAP_PATH = ROOT / ".system" / "memory" / "strategy" / "cfa-legacy-to-official-enrichment-map.md"
ROADMAP_PATH = ROOT / "docs" / "cfa-knowledge-base-display-evolution.md"


SUBJECT_CORE = {
    "Quantitative Methods": "把投资问题翻译成收益率、现金流、统计推断和模型检验。",
    "Economics": "用市场结构、周期、政策、贸易和汇率解释宏观环境对资产价格的影响。",
    "Corporate Issuers": "理解公司组织、治理、营运资本、资本配置与商业模式如何影响价值创造。",
    "Financial Statement Analysis": "把三张报表转成可比较、可预测、可质疑的经营证据。",
    "Equity Investments": "理解股票市场结构、行业公司分析和权益估值工具。",
    "Fixed Income": "从债券现金流、收益率曲线、久期凸性、信用和证券化拆解固定收益风险回报。",
    "Derivatives": "用无套利、复制和工具结构理解远期、期货、互换、期权的风险转移。",
    "Alternative Investments": "识别另类投资结构、绩效、私募、实物资产、对冲基金与数字资产特征。",
    "Portfolio Management": "把风险收益、组合构建、行为偏差和风险管理连接成投资流程。",
    "Ethical and Professional Standards": "用 Code and Standards 判断专业行为、利益冲突、客户责任与合规边界。",
}


SUBJECT_FRAMEWORK = {
    "Quantitative Methods": "定义变量 -> 选择统计/现金流工具 -> 计算结果 -> 解释经济含义 -> 检查假设",
    "Economics": "识别市场/宏观变量 -> 判断冲击方向 -> 连接政策反应 -> 推导价格/产出/汇率影响",
    "Corporate Issuers": "识别公司决策 -> 判断现金流与风险影响 -> 连接治理约束 -> 评估价值后果",
    "Financial Statement Analysis": "定位报表项目 -> 调整可比性 -> 计算指标 -> 解释质量与持续性",
    "Equity Investments": "界定市场与行业 -> 分析公司竞争力 -> 选择估值模型 -> 做敏感性判断",
    "Fixed Income": "拆现金流 -> 选折现率/曲线 -> 估值 -> 度量利率/信用/期权风险",
    "Derivatives": "识别标的与到期现金流 -> 建立无套利关系 -> 定价/估值 -> 判断风险暴露",
    "Alternative Investments": "识别资产结构 -> 判断流动性/估值/费用 -> 解释收益来源 -> 比较风险约束",
    "Portfolio Management": "设定目标约束 -> 估计风险收益 -> 构建组合 -> 监控偏差与风险",
    "Ethical and Professional Standards": "识别相关标准 -> 判断责任对象 -> 找冲突/披露/忠诚义务 -> 选择最保守合规动作",
}


TERM_TRANSLATIONS = {
    "Rates and Returns": ("利率与收益率", "把现金流的时间价值、风险补偿和投资表现放到同一套语言中比较。"),
    "Time Value of Money": ("货币时间价值", "今天的一元钱与未来的一元钱价值不同，必须用折现或复利转换。"),
    "Present Value": ("现值", "未来现金流按要求回报率折现到今天的价值。"),
    "Future Value": ("终值", "当前金额按复利增长到未来时点的价值。"),
    "Money-Weighted Return": ("资金加权收益率", "把投资者现金流时间点纳入计算的 IRR 式收益率。"),
    "Time-Weighted Return": ("时间加权收益率", "剔除外部现金流影响，更适合评价投资经理表现。"),
    "Statistical Measures": ("统计度量", "用均值、离散程度、偏度和峰度描述收益分布。"),
    "Standard Deviation": ("标准差", "衡量收益围绕均值波动的典型幅度。"),
    "Correlation": ("相关系数", "衡量两个变量线性同向或反向变化的程度。"),
    "Hypothesis Testing": ("假设检验", "用样本证据判断总体命题是否应被拒绝。"),
    "Regression": ("回归", "用一个或多个解释变量估计因变量的平均变化关系。"),
    "Big Data": ("大数据", "用更高维、非结构化或高频数据改进投资判断。"),
    "Demand and Supply": ("供给与需求", "用价格、数量和弹性解释市场均衡变化。"),
    "Business Cycles": ("商业周期", "经济活动围绕趋势扩张和收缩的阶段性波动。"),
    "Monetary Policy": ("货币政策", "央行通过利率、流动性和预期管理影响经济。"),
    "Fiscal Policy": ("财政政策", "政府通过税收、支出和赤字影响总需求与资源配置。"),
    "Exchange Rates": ("汇率", "两种货币之间的相对价格。"),
    "Financial Statements": ("财务报表", "资产负债表、利润表和现金流量表的统称。"),
    "Income Statement": ("利润表", "解释收入、费用和盈利能力的期间报表。"),
    "Balance Sheet": ("资产负债表", "展示某一时点资产、负债和权益的存量结构。"),
    "Cash Flow": ("现金流", "企业现金流入和流出的真实资金轨迹。"),
    "Inventories": ("存货", "企业用于销售或生产的库存资产。"),
    "Long-Lived Assets": ("长期资产", "使用期超过一个经营周期的资产。"),
    "Deferred Taxes": ("递延所得税", "会计利润与税务利润差异形成的未来税务影响。"),
    "Corporate Governance": ("公司治理", "约束管理层、董事会和股东之间权责关系的制度。"),
    "Capital Budgeting": ("资本预算", "评估长期投资项目是否创造价值。"),
    "Working Capital": ("营运资本", "流动资产和流动负债管理对运营现金流的影响。"),
    "Market Organization": ("市场组织", "交易场所、订单机制和参与者的结构。"),
    "Industry Analysis": ("行业分析", "判断行业结构、竞争强度和盈利持续性。"),
    "Equity Valuation": ("权益估值", "估计普通股内在价值的模型和比较方法。"),
    "Fixed Income": ("固定收益", "以约定现金流为核心的债务类证券。"),
    "Bond Valuation": ("债券估值", "用现金流和折现率估计债券价格。"),
    "Yield": ("收益率", "把债券价格与未来现金流连接起来的回报度量。"),
    "Duration": ("久期", "衡量债券价格对利率变化敏感度的核心指标。"),
    "Convexity": ("凸性", "修正久期线性近似不足的二阶价格敏感度。"),
    "Credit Risk": ("信用风险", "发行人无法按时足额履约的风险。"),
    "Securitization": ("证券化", "把资产池现金流重组为可交易证券的过程。"),
    "Forward": ("远期", "双方约定未来按固定价格交易标的的合约。"),
    "Futures": ("期货", "交易所标准化、每日盯市的远期类合约。"),
    "Swap": ("互换", "双方交换一系列未来现金流的合约。"),
    "Option": ("期权", "买方拥有权利但无义务，卖方承担相应义务的衍生品。"),
    "Private Capital": ("私募资本", "非公开市场股权或债务投资。"),
    "Real Estate": ("房地产", "以不动产及相关现金流为基础的另类投资。"),
    "Hedge Funds": ("对冲基金", "采用更灵活策略、杠杆和做空工具的集合投资工具。"),
    "Digital Assets": ("数字资产", "基于分布式账本或加密网络的资产形态。"),
    "Portfolio": ("投资组合", "多个资产或证券按权重组成的整体。"),
    "CAPM": ("资本资产定价模型", "用系统性风险解释预期收益的均衡模型。"),
    "Efficient Frontier": ("有效前沿", "在给定风险下收益最高、或给定收益下风险最低的组合集合。"),
    "Risk Management": ("风险管理", "识别、度量、监控并应对风险的流程。"),
    "Ethics": ("伦理", "专业行为、客户利益、市场诚信和合规责任的规范体系。"),
    "Code and Standards": ("职业道德准则与行为标准", "CFA Institute 对会员和候选人的核心行为要求。"),
    "GIPS": ("全球投资业绩标准", "用于投资业绩展示公平性和可比性的自愿标准。"),
}


FORMULA_BANK = {
    "Quantitative Methods": [
        ("HPR", "HPR = (P1 - P0 + D1) / P0", "持有期收益率，注意价格变动和期间现金流都要纳入。"),
        ("Effective annual rate", "EAR = (1 + periodic rate)^m - 1", "不同复利频率比较时必须转成同一口径。"),
        ("Present value", "PV = FV / (1 + r)^N", "折现率越高，现值越低。"),
        ("Variance", "σ² = Σ(xi - xbar)² / (n - 1)", "样本方差分母通常用 n-1。"),
        ("Test statistic", "test statistic = (sample statistic - hypothesized value) / standard error", "先判断单尾/双尾，再与临界值或 p-value 比较。"),
        ("Simple regression", "Yi = b0 + b1Xi + ei", "b1 表示 X 增加 1 单位时 Y 的预期变化。"),
    ],
    "Economics": [
        ("Elasticity", "elasticity = %ΔQ / %ΔP", "绝对值大于 1 表示富有弹性。"),
        ("GDP identity", "Y = C + I + G + (X - M)", "支出法 GDP 的基本分解。"),
        ("Money multiplier", "money multiplier ≈ 1 / reserve requirement", "考试更常考方向判断而非复杂推导。"),
        ("Interest parity", "forward premium/discount links interest rate differentials", "汇率题要先确认 base/price currency。"),
    ],
    "Corporate Issuers": [
        ("NPV", "NPV = Σ CFt / (1 + r)^t - initial investment", "NPV > 0 表示项目预计创造价值。"),
        ("WACC", "WACC = wd rd(1 - t) + wp rp + we re", "资本结构权重要用市场价值口径。"),
        ("Operating cycle", "operating cycle = days inventory + days receivables", "现金周转题要分清 operating cycle 和 cash conversion cycle。"),
    ],
    "Financial Statement Analysis": [
        ("Current ratio", "current assets / current liabilities", "衡量短期偿债能力，但不等于现金质量。"),
        ("Gross margin", "gross profit / revenue", "可用于比较定价能力和成本压力。"),
        ("ROE", "net income / average equity", "可用 DuPont 分解定位盈利、效率和杠杆来源。"),
        ("CFO", "cash flow from operations", "盈利质量题常比较 CFO 与 net income。"),
    ],
    "Equity Investments": [
        ("Dividend discount model", "V0 = D1 / (r - g)", "只适用于稳定增长且 r > g 的情形。"),
        ("P/E", "price per share / earnings per share", "比较估值要注意盈利质量和周期位置。"),
        ("Market capitalization", "price per share × shares outstanding", "常用于指数权重和规模判断。"),
    ],
    "Fixed Income": [
        ("Bond price", "P = Σ C/(1+y)^t + FV/(1+y)^N", "债券价格等于未来现金流现值。"),
        ("Full price", "full price = clean price + accrued interest", "报价通常是 clean price，结算用 full price。"),
        ("Modified duration", "ModDur = MacDur / (1 + y/m)", "近似衡量收益率变化 1 单位时价格百分比变化。"),
        ("Approximate convexity", "(V- + V+ - 2V0) / (V0 × Δy²)", "凸性修正久期的一阶近似误差。"),
        ("Credit loss", "expected loss = probability of default × loss given default", "信用题要分清 PD、LGD、recovery rate。"),
    ],
    "Derivatives": [
        ("Forward value", "Vt = St - PV(forward price)", "远期合约价值随标的价格和折现变化。"),
        ("Put-call parity", "c + PV(X) = p + S", "欧式期权无套利关系，高频判断式。"),
        ("Option payoff", "call = max(0, S - X), put = max(0, X - S)", "先画到期收益，再考虑期权费。"),
    ],
    "Alternative Investments": [
        ("Management fee", "fee base × fee rate", "私募和对冲基金题要区分管理费和激励费。"),
        ("NAV", "assets - liabilities", "基金估值与费用计算的基础口径。"),
        ("Cap rate", "NOI / property value", "房地产估值中常用于收入资本化法。"),
    ],
    "Portfolio Management": [
        ("Portfolio return", "Rp = Σ wi Ri", "组合收益是资产收益的加权平均。"),
        ("Portfolio variance", "σp² = w1²σ1² + w2²σ2² + 2w1w2ρ12σ1σ2", "相关性越低，分散化收益越明显。"),
        ("Sharpe ratio", "(Rp - Rf) / σp", "用总风险衡量超额收益效率。"),
        ("CAPM", "E(Ri) = Rf + βi[E(Rm)-Rf]", "只补偿系统性风险。"),
    ],
    "Ethical and Professional Standards": [
        ("Ethics decision rule", "identify duty -> disclose conflicts -> protect client interests -> document action", "伦理题更像判断流程，不是公式题。"),
        ("GIPS scope", "firm definition -> composite construction -> performance presentation", "GIPS 题要先判断公司定义和组合口径。"),
    ],
}


EXAM_VERBS = {
    "calculate": "计算并解释数值结果",
    "interpret": "解释结果的投资含义",
    "compare": "比较相似概念的适用条件与差异",
    "describe": "描述定义、流程和适用场景",
    "explain": "解释机制、原因和后果",
    "evaluate": "评价优缺点、限制和决策含义",
    "identify": "识别题干中的关键事实和触发条件",
    "determine": "根据条件判断正确结论",
    "recommend": "给出符合约束的行动建议",
}


@dataclass
class LegacyMatch:
    path: Path
    score: float
    confidence: str
    title: str
    headings: list[str]
    highlights: list[str]
    formulas: list[str]
    traps: list[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def slug_tokens(value: str) -> set[str]:
    return {
        t.lower()
        for t in re.findall(r"[A-Za-z][A-Za-z0-9]+", value)
        if len(t) > 2 and t.lower() not in {"module", "with", "and", "the", "for", "from", "into", "introduction"}
    }


def clean_module_name(official_module: str) -> str:
    return re.sub(r"^Module\s+\d+:\s*", "", official_module).strip()


def module_number(module_id: str) -> int:
    match = re.search(r"(\d+)", module_id)
    return int(match.group(1)) if match else 0


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[: end + 4].strip() + "\n", text[end + 4 :].lstrip("\n")
    return "", text


def parse_page_items(page_items: Iterable[str]) -> list[str]:
    result = []
    for item in page_items:
        if "|" in item:
            result.append(item.split("|", 1)[1].strip())
        elif not item.lower().startswith("learning outcomes"):
            result.append(item.strip())
    return result


def detect_difficulty(subject: str, module_name: str, los: list[str]) -> str:
    text = " ".join([subject, module_name, *los]).lower()
    if any(k in text for k in ["calculate", "regression", "valuation", "yield", "duration", "convexity", "hypothesis", "return", "present value", "probability"]):
        return "计算+解释"
    if any(k in text for k in ["ethic", "standard", "governance", "geopolitical", "business cycle", "market organization"]):
        return "概念+案例判断"
    return "概念+应用"


def los_action(los_text: str) -> str:
    found = [cn for verb, cn in EXAM_VERBS.items() if re.search(rf"\b{verb}\b", los_text, flags=re.I)]
    return "；".join(found[:3]) if found else "识别概念、解释机制并应用到题干。"


def english_terms(module_name: str, page_topics: list[str], subject: str) -> list[tuple[str, str, str]]:
    candidates = [module_name, *page_topics]
    if subject in {"Ethical and Professional Standards", "Fixed Income", "Portfolio Management"}:
        candidates.append(subject)

    terms: list[tuple[str, str, str]] = []
    seen = set()
    for candidate in candidates:
        cleaned = re.sub(r"^\d+\.\d+\s*\|\s*", "", candidate).strip()
        parts = [cleaned]
        if ":" in cleaned:
            parts.append(cleaned.split(":", 1)[0].strip())
        for term in parts:
            if len(term) < 4 or term.lower() in seen:
                continue
            seen.add(term.lower())
            zh, expl = TERM_TRANSLATIONS.get(term, ("核心术语", "本模块关键词，用于定位 LOS、题干条件和解题动作。"))
            terms.append((term, zh, expl))

    for known, (zh, expl) in TERM_TRANSLATIONS.items():
        if known.lower() in " ".join(candidates).lower() and known.lower() not in seen:
            seen.add(known.lower())
            terms.append((known, zh, expl))
    return terms[:8]


def formula_rows(subject: str, module_name: str, los: list[str]) -> list[tuple[str, str, str]]:
    bank = FORMULA_BANK.get(subject, [])
    text = " ".join([module_name, *los]).lower()
    selected = []
    for name, formula, note in bank:
        words = slug_tokens(name)
        if words and (words & slug_tokens(text)):
            selected.append((name, formula, note))
    if not selected:
        if any(v in text for v in ["calculate", "compute", "estimate", "valuation", "return", "yield", "duration", "ratio", "value"]):
            selected = bank[:3]
        else:
            selected = []
    return selected[:5]


def extract_legacy_files(subject_dir: Path) -> list[Path]:
    sync_dir = subject_dir / "_legacy" / "2026-05-26-official-sync"
    if not sync_dir.exists():
        return []
    return sorted(sync_dir.rglob("*.md"))


def title_from_text(path: Path, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    return path.stem


def legacy_headings(text: str) -> list[str]:
    headings = []
    for line in text.splitlines():
        if re.match(r"^#{1,4}\s+", line):
            heading = re.sub(r"^#{1,4}\s+", "", line).strip()
            if heading and not heading.lower().startswith("module "):
                headings.append(heading)
    return headings[:18]


def useful_lines(text: str, patterns: list[str], limit: int) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip().strip("- ").strip()
        if not line or line.startswith("|") or len(line) > 180:
            continue
        if any(re.search(p, line, flags=re.I) for p in patterns):
            normalized = re.sub(r"\s+", " ", line)
            if normalized not in lines:
                lines.append(normalized)
        if len(lines) >= limit:
            break
    return lines


def score_legacy(text_blob: str, path: Path, module_name: str, page_topics: list[str], los: list[str]) -> float:
    source = " ".join([path.stem, text_blob[:4000]])
    target = " ".join([module_name, *page_topics, *los])
    source_tokens = slug_tokens(source)
    target_tokens = slug_tokens(target)
    if not source_tokens or not target_tokens:
        return 0.0
    overlap = len(source_tokens & target_tokens) / max(1, len(target_tokens))
    seq = SequenceMatcher(None, path.stem.lower(), module_name.lower()).ratio()
    return round(min(1.0, overlap * 0.75 + seq * 0.25), 3)


def confidence(score: float) -> str:
    if score >= 0.42:
        return "high"
    if score >= 0.25:
        return "medium"
    return "low"


def build_legacy_matches(registry: dict) -> dict[tuple[str, str], list[LegacyMatch]]:
    matches: dict[tuple[str, str], list[LegacyMatch]] = defaultdict(list)
    for subject, subject_data in registry["subjects"].items():
        subject_dir = ROOT / "CFA_tier1" / subject_data["directory"]
        legacy_paths = extract_legacy_files(subject_dir)
        if not legacy_paths:
            continue
        cache = [(path, read_text(path)) for path in legacy_paths]
        for module in subject_data["modules"]:
            module_name = clean_module_name(module["official_module"])
            page_topics = parse_page_items(module.get("page_items", []))
            scored: list[LegacyMatch] = []
            for path, text in cache:
                score = score_legacy(text, path, module_name, page_topics, module.get("los", []))
                conf = confidence(score)
                headings = legacy_headings(text)
                scored.append(
                    LegacyMatch(
                        path=path,
                        score=score,
                        confidence=conf,
                        title=title_from_text(path, text),
                        headings=headings,
                        highlights=useful_lines(text, [r"定义", r"核心", r"must", r"important", r"关键", r"高频", r"判断"], 5),
                        formulas=useful_lines(text, [r"=", r"公式", r"calculate", r"ratio", r"return", r"yield"], 4),
                        traps=useful_lines(text, [r"陷阱", r"易错", r"注意", r"不要", r"confus", r"warning"], 4),
                    )
                )
            matches[(subject, module["module"])] = sorted(scored, key=lambda item: item.score, reverse=True)[:5]
    return matches


def wiki_link(filename: str) -> str:
    return f"[[{Path(filename).stem}]]"


def module_frontmatter(subject: str, subject_data: dict, module: dict, difficulty: str) -> str:
    module_name = clean_module_name(module["official_module"])
    los_count = len(module.get("los", []))
    return f"""---
title: "{module['module']}: {module_name}"
description: "CFA Level I 2026 {subject} 官方模块笔记：中文主线、英文术语、编号知识树、LOS 对齐"
subject: "{subject}"
topic_area: "{subject_data['directory']}"
level: "CFA Level I"
exam_year: 2026
exam_weight: "{subject_data.get('exam_weight', '')}"
module: "{module['module']}"
official_module: "{module['official_module']}"
los_count: {los_count}
difficulty: "{difficulty}"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - {subject_data['directory']}
---
"""


def render_official_structure(page_items: list[str]) -> str:
    if not page_items:
        return "- 暂无官方页面条目。\n"
    return "\n".join(f"- {item}" for item in page_items) + "\n"


def render_los(los: list[str]) -> str:
    if not los:
        return "- 暂无 LOS。请回到官方 registry 核验。\n"
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(los, 1)) + "\n"


def tree_topics(module_idx: int, module_name: str, page_topics: list[str], los: list[str]) -> list[tuple[str, str]]:
    topics = page_topics[:5]
    if len(topics) < 3:
        topics.extend([f"LOS {i}: {los_text[:68]}" for i, los_text in enumerate(los[: 5 - len(topics)], 1)])
    if not topics:
        topics = [module_name]
    return [(f"{module_idx}.{i}", topic) for i, topic in enumerate(topics[:5], 1)]


def render_module_tree(module_idx: int, module_name: str, page_topics: list[str], los: list[str]) -> str:
    lines = [f"{module_idx}. {module_name}"]
    topics = tree_topics(module_idx, module_name, page_topics, los)
    for number, topic in topics:
        lines.append(f"├─ {number} {topic}")
        lines.append(f"│  ├─ {number}.1 定义/识别：掌握题干关键词与适用条件")
        lines.append(f"│  └─ {number}.2 应用/判断：把概念或公式转成解题动作")
    return "```text\n" + "\n".join(lines) + "\n```\n"


def render_knowledge_details(subject: str, module_idx: int, module_name: str, page_topics: list[str], los: list[str], terms: list[tuple[str, str, str]], legacy: list[LegacyMatch]) -> str:
    sections = []
    topics = tree_topics(module_idx, module_name, page_topics, los)
    for i, (number, topic) in enumerate(topics, 1):
        related_los = los[i - 1] if i - 1 < len(los) else (los[0] if los else "")
        sections.append(f"### {number} {topic}\n")
        sections.append(f"- **中文主线**：本节点解决 `{topic}` 在 {subject} 中的定义、适用条件和考试判断。先确认题干问的是概念识别、机制解释、数值计算还是优劣比较。\n")
        if related_los:
            sections.append(f"- **对应 LOS 动作**：{los_action(related_los)}；官方表述为：`{related_los}`。\n")
        if terms:
            term, zh, explanation = terms[(i - 1) % len(terms)]
            sections.append(f"- **核心词汇**：**{term}（{zh}）**：{explanation}\n")
        sections.append("- **解题输出**：用一句话写出结论，再补充计算口径、方向判断或限制条件，避免只背定义。\n")
        sections.append("\n")

    high = [m for m in legacy if m.confidence == "high"]
    if high:
        sections.append(f"### {module_idx}.9 Legacy 补强要点\n")
        for match in high[:2]:
            bits = match.highlights or match.headings[:3] or [match.title]
            sections.append(f"- 来自 `{match.path.name}`：{'; '.join(bits[:3])}。\n")
        sections.append("\n")
    return "".join(sections)


def render_formula_section(subject: str, module_name: str, los: list[str], rows: list[tuple[str, str, str]]) -> str:
    if not rows:
        return f"本模块以概念判断为主，无核心计算公式。复习时把 `{module_name}` 的定义、触发条件、优缺点和例外情形整理成判断清单。\n"
    table = ["| 工具 / Formula | 公式或框架 | 中文解释与注意点 |", "|---|---|---|"]
    for name, formula, note in rows:
        table.append(f"| {name} | `{formula}` | {note} |")
    table.append("")
    table.append("计算题通用检查：单位一致、时间口径一致、现金流方向一致；解释题要说明结果代表的经济含义。")
    return "\n".join(table) + "\n"


def adjacent_modules(subject_data: dict, module_id: str) -> tuple[dict | None, dict | None]:
    modules = subject_data["modules"]
    idx = next((i for i, m in enumerate(modules) if m["module"] == module_id), None)
    if idx is None:
        return None, None
    prev_m = modules[idx - 1] if idx > 0 else None
    next_m = modules[idx + 1] if idx + 1 < len(modules) else None
    return prev_m, next_m


def render_legacy_section(matches: list[LegacyMatch]) -> str:
    high = [m for m in matches if m.confidence == "high"]
    if not high:
        medium = [m for m in matches if m.confidence == "medium"]
        if medium:
            names = ", ".join(f"`{m.path.name}` ({m.score})" for m in medium[:3])
            return f"本次未发现可直接高置信合并的 legacy 内容。中置信候选已记录到 enrichment map：{names}。后续如需人工补强，应先核验其是否符合 2026 官方 LOS。\n"
        return "本次未发现可映射的 legacy 内容；当前内容以官方 registry、LOS 和模块结构为准。\n"

    lines = ["以下内容来自高置信 legacy 映射，已作为补强入口保留；若与官方 2026 LOS 冲突，以官方内容为准。\n"]
    for match in high[:3]:
        lines.append(f"### 来源：{match.path.name}（confidence {match.score}）\n")
        if match.headings:
            lines.append("- **可复用结构**：" + "；".join(match.headings[:6]) + "\n")
        if match.highlights:
            lines.append("- **高价值要点**：" + "；".join(match.highlights[:4]) + "\n")
        if match.formulas:
            lines.append("- **公式/计算线索**：" + "；".join(match.formulas[:3]) + "\n")
        if match.traps:
            lines.append("- **易错提示**：" + "；".join(match.traps[:3]) + "\n")
        lines.append("\n")
    return "".join(lines)


def render_module(subject: str, subject_data: dict, module: dict, matches: list[LegacyMatch]) -> str:
    module_idx = module_number(module["module"])
    module_name = clean_module_name(module["official_module"])
    page_topics = parse_page_items(module.get("page_items", []))
    los = module.get("los", [])
    difficulty = detect_difficulty(subject, module_name, los)
    terms = english_terms(module_name, page_topics, subject)
    formulas = formula_rows(subject, module_name, los)
    prev_m, next_m = adjacent_modules(subject_data, module["module"])
    frontmatter = module_frontmatter(subject, subject_data, module, difficulty)

    los_rows = ["| LOS | 官方要求 | 中文学习动作 | 做题输出 |", "|---|---|---|---|"]
    for i, los_text in enumerate(los, 1):
        los_rows.append(f"| {module_idx}.{i} | {los_text} | {los_action(los_text)} | 写出结论、依据和限制条件。 |")

    term_rows = "\n".join(f"- **{term}（{zh}）**：{expl}" for term, zh, expl in terms)
    prev_link = wiki_link(prev_m["filename"]) if prev_m else "本科目起点"
    next_link = wiki_link(next_m["filename"]) if next_m else "本科目收束模块"

    body = f"""# {module['module']}: {module_name}

> **模块定位**：{SUBJECT_CORE.get(subject, '')} 本模块聚焦 **{module_name}**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

{render_official_structure(module.get('page_items', []))}
## Learning Outcome Statements

{render_los(los)}
---

## 1. 模块定位

### {module_idx}.1 学习任务
- **核心问题**：考试希望你用 `{module_name}` 解释什么、计算什么、或判断什么。
- **输入信息**：题干事实、数据、定义、假设、限制条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### {module_idx}.2 考试角色
- **难度类型**：{difficulty}。
- **高频题型**：定义辨析、情境判断、计算解释、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；不要在还没识别题型时直接套公式。

### {module_idx}.3 关键英文术语
{term_rows if term_rows else "- 本模块术语以官方 LOS 和页面标题为准，复习时自行补充题库中反复出现的英文关键词。"}

## 2. 官方 LOS 对应学习目标

{chr(10).join(los_rows)}

## 3. 核心知识树

{render_module_tree(module_idx, module_name, page_topics, los)}
## 4. 知识点详解

{render_knowledge_details(subject, module_idx, module_name, page_topics, los, terms, matches)}
## 5. 关键公式与计算框架

{render_formula_section(subject, module_name, los, formulas)}
## 6. 常见考点与解题思路

- **考点 1：定义与边界**。看到英文术语时，先翻译成中文含义，再判断它解决的是收益、风险、估值、披露、治理还是合规问题。
- **考点 2：方向判断**。如果题干改变一个变量，先写出经济直觉，再用公式或框架验证方向。
- **考点 3：比较题**。用“适用条件 - 优点 - 局限 - 典型陷阱”四列比较，不要只背定义。
- **考点 4：解释题**。答案必须包含结果含义，例如“更高/更低意味着什么”，以及是否需要补充假设。

## 7. 易错点与考试陷阱

- **中英文错配**：看到 `{module_name}` 相关英文词，不要只按中文直觉判断，先回到官方定义。
- **LOS 动词误读**：`calculate` 要算并解释，`compare` 要列差异，`evaluate` 要给判断依据。
- **口径混用**：时间、收益率、现金流、报告期、组合权重或会计口径不一致时，结论很容易反向。
- **孤立背诵**：本模块知识点通常会与前后模块联动，刷题时记录它触发了哪个上游概念。

## 8. 跨模块关联

- **上游模块**：{prev_link}。它提供本模块所需的定义、变量或基础框架。
- **下游模块**：{next_link}。它通常会把本模块工具用于更复杂的估值、风险或情境判断。
- **跨科连接**：与 Portfolio Management 的风险收益框架、Financial Statement Analysis 的证据质量、Ethics 的合规判断保持连接。

## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义和用途。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

{render_legacy_section(matches)}
"""
    return frontmatter + "\n" + body.rstrip() + "\n"


def moc_filename(subject_dir: Path, subject: str) -> Path:
    files = sorted(subject_dir.glob("00-*-MOC.md"))
    if files:
        return files[0]
    return subject_dir / f"00-{subject.replace(' ', '-')}-MOC.md"


def render_moc(subject: str, subject_data: dict, matches_by_module: dict[tuple[str, str], list[LegacyMatch]]) -> str:
    directory = subject_data["directory"]
    weight = subject_data.get("exam_weight", "")
    modules = subject_data["modules"]
    frontmatter = f"""---
title: "00-{subject}-MOC"
description: "CFA Level I 2026 {subject} 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "{subject}"
topic_area: "{directory}"
level: "CFA Level I"
exam_year: 2026
exam_weight: "{weight}"
module_count: {len(modules)}
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - {directory}
---
"""
    nav = ["| 编号 | 官方 Module | 难度 | 必考点 | 模块链接 |", "|---|---|---|---|---|"]
    for m in modules:
        module_name = clean_module_name(m["official_module"])
        page_topics = parse_page_items(m.get("page_items", []))
        difficulty = detect_difficulty(subject, module_name, m.get("los", []))
        focus = " / ".join(page_topics[:2]) if page_topics else "LOS 对齐学习"
        nav.append(f"| {m['module']} | {module_name} | {difficulty} | {focus} | {wiki_link(m['filename'])} |")

    tree_lines = [f"{subject} ({weight})"]
    for m in modules:
        idx = module_number(m["module"])
        module_name = clean_module_name(m["official_module"])
        tree_lines.append(f"├─ {idx}. {module_name}")
        for number, topic in tree_topics(idx, module_name, parse_page_items(m.get("page_items", [])), m.get("los", []))[:3]:
            tree_lines.append(f"│  ├─ {number} {topic}")

    dependencies = []
    for i, m in enumerate(modules):
        module_name = clean_module_name(m["official_module"])
        prev_name = clean_module_name(modules[i - 1]["official_module"]) if i > 0 else "本科目入口"
        next_name = clean_module_name(modules[i + 1]["official_module"]) if i + 1 < len(modules) else "本科目总结"
        dependencies.append(f"- **{m['module']} {module_name}**：承接 `{prev_name}`，输出到 `{next_name}`。")

    formulas = FORMULA_BANK.get(subject, [])
    formula_table = ["| 编号 | 工具 / Formula | 中文用途 |", "|---|---|---|"]
    if formulas:
        for i, (name, formula, note) in enumerate(formulas, 1):
            formula_table.append(f"| F{i} | `{name}: {formula}` | {note} |")
    else:
        formula_table.append("| F1 | 概念判断框架 | 本科目以定义、责任、流程和边界判断为主。 |")

    legacy_lines = []
    high_count = 0
    medium_count = 0
    for m in modules:
        module_matches = matches_by_module.get((subject, m["module"]), [])
        high_count += sum(1 for item in module_matches if item.confidence == "high")
        medium_count += sum(1 for item in module_matches if item.confidence == "medium")
    legacy_lines.append(f"- 本科目高置信 legacy 映射：{high_count} 条；中置信候选：{medium_count} 条。")
    legacy_lines.append(f"- 详细来源与处理建议见 [[cfa-legacy-to-official-enrichment-map]]。")
    legacy_lines.append("- `_legacy` 只作为补强来源，不作为最终学习入口；若与官方 2026 LOS 冲突，以 registry 和官方 Topic Outline 为准。")

    return frontmatter + f"""
# {subject} MOC

> **一句话核心**：{SUBJECT_CORE.get(subject, '')}

---

## 1. 科目定位

- **考试权重**：{weight}
- **官方模块数**：{len(modules)}
- **主线框架**：{SUBJECT_FRAMEWORK.get(subject, '识别概念 -> 应用框架 -> 解释结果 -> 检查限制条件')}
- **使用方式**：先从官方模块导航进入，再用编号知识树做主动回忆，最后用公式/陷阱清单做考前压缩。

## 2. 官方模块导航

{chr(10).join(nav)}

## 3. 核心知识树

```text
{chr(10).join(tree_lines)}
```

## 4. 跨模块依赖关系

{chr(10).join(dependencies)}

## 5. 核心对比专题

- **概念 vs 应用**：先确认官方定义，再把定义放入题干情境判断。
- **计算 vs 解释**：计算结果只是中间步骤，CFA Level I 经常要求解释方向、限制和投资含义。
- **静态知识 vs 决策流程**：把每个模块压缩成“输入 -> 工具 -> 输出 -> 陷阱”的流程。
- **英文术语 vs 中文理解**：英文保留用于识题，中文解释用于防止机械背诵。

## 6. 公式与框架速查

{chr(10).join(formula_table)}

## 7. 高频考试陷阱

- **模块名和旧笔记不一致**：以 2026 官方 module 名称、编号和顺序为准。
- **只背公式不解释**：凡是 `calculate and interpret`，必须同时会算和解释。
- **忽略 LOS 动词**：`describe`、`explain`、`compare`、`evaluate` 对答案深度要求不同。
- **跨模块断裂**：做错题时记录它关联到哪个 MOC 节点，必要时触发 MOC gap review。

## 8. 通用分析框架

1. **识别任务**：读 LOS 动词和题干问法。
2. **定位节点**：回到 `## 3. 核心知识树` 的编号节点。
3. **选择工具**：概念框架、公式、表格比较或合规流程。
4. **输出结论**：中文结论 + 英文关键词 + 必要限制条件。
5. **复盘缺口**：若错因重复出现，进入 `.system/events/` 和 `.system/memory/` 闭环。

## 9. 学习路径建议

- **第一轮：结构对齐**。按模块顺序读官方结构和 LOS，不急着刷难题。
- **第二轮：主动回忆**。遮住解释，只看编号知识树说出定义、公式和陷阱。
- **第三轮：题目驱动**。把错题回填到对应模块和 MOC 节点，形成可复用 fix rule。
- **考前压缩**。只保留高频术语、公式/框架、易错点、跨模块依赖和错题触发点。

## 10. Legacy 内容治理

{chr(10).join(legacy_lines)}
""".rstrip() + "\n"


def render_legacy_map(registry: dict, matches_by_module: dict[tuple[str, str], list[LegacyMatch]]) -> str:
    lines = [
        "---",
        'title: "CFA Legacy to Official Enrichment Map"',
        'description: "Legacy 笔记到 CFA Level I 2026 官方 module 的映射、置信度和处理建议"',
        "note_type: strategy",
        "status: active",
        "updated: 2026-05-26",
        "---",
        "",
        "# CFA Legacy to Official Enrichment Map",
        "",
        "> 本文档是治理资产，不是学习入口。高置信内容已进入对应官方 module 的 `Legacy Notes Integrated`；中低置信内容只作为人工审计候选。",
        "",
        "## 1. 处理规则",
        "",
        "- **high**：可作为补强内容进入官方 module，但仍以 2026 LOS 为边界。",
        "- **medium**：只记录候选，不强行合并，后续人工核验后再处理。",
        "- **low**：暂不使用，除非后续发现官方模块缺口需要重新检索。",
        "- `_legacy` 不是最终学习入口；`CFA_tier1/` 官方 module 与 MOC 是投影视图，source of truth 仍是 registry、`.system/events/`、`.system/memory/`。",
        "",
        "## 2. 映射总览",
        "",
        "| Subject | Official Module | Current File | Legacy Sources | Confidence | Reusable Sections | Action |",
        "|---|---|---|---|---|---|---|",
    ]
    for subject, subject_data in registry["subjects"].items():
        for module in subject_data["modules"]:
            module_name = clean_module_name(module["official_module"])
            matches = matches_by_module.get((subject, module["module"]), [])
            selected = [m for m in matches if m.confidence in {"high", "medium"}][:3]
            if not selected and matches:
                selected = matches[:1]
            if not selected:
                source = "无"
                conf = "none"
                sections = "无"
                action = "仅保留官方内容"
            else:
                source = "<br>".join(f"`{m.path.name}` ({m.score})" for m in selected)
                conf = "<br>".join(m.confidence for m in selected)
                sections = "<br>".join("; ".join(m.headings[:3]) if m.headings else m.title for m in selected)
                if any(m.confidence == "high" for m in selected):
                    action = "已写入 module 的 Legacy Notes Integrated"
                elif any(m.confidence == "medium" for m in selected):
                    action = "人工审计后再决定是否补强"
                else:
                    action = "暂不合并"
            lines.append(f"| {subject} | {module['module']} {module_name} | `{module['filename']}` | {source} | {conf} | {sections} | {action} |")

    lines.extend(
        [
            "",
            "## 3. 后续审计清单",
            "",
            "- 对 medium 映射逐条核验是否仍符合 2026 official module 名称、顺序和 LOS。",
            "- 如果 legacy 内容只是旧模块拆分方式，不产生新的定义、公式、陷阱或例题框架，则不晋升。",
            "- 如果错题反复暴露同一 MOC 缺口，先写入 `.system/memory/strategy/moc-gap-review.md`，再由 Codex 二次判断是否修改 MOC。",
        ]
    )
    return "\n".join(lines) + "\n"


def render_roadmap() -> str:
    directions = [
        ("Obsidian Canvas 知识地图", "把 10 科 MOC、93 个 module、错题 pattern 连成可视化地图。", "复习全局结构、发现跨模块依赖。", "官方 registry、MOC、module frontmatter、.system/memory/patterns", "中：需要稳定节点 ID 与 Canvas JSON 生成脚本。", "P1", "Canvas 容易变成手工图；必须可重复生成。"),
        ("Dataview / Dashboard 自动聚合", "按 topic、LOS、错因、复习日期自动汇总当前弱点。", "每日复盘、周度 pattern mining、考前 brief。", ".system/events/catalog.sqlite3、.system/memory、CFA_tier1/dashboard", "中：需要 frontmatter 规范和导出脚本。", "P1", "不要让 dashboard 成为 source of truth。"),
        ("静态网站或本地 Web app", "把 Markdown 投影为可搜索、可筛选、可跳转的学习应用。", "长时间复习、手机/平板阅读、跨模块检索。", "registry、CFA_tier1、.system/memory 生成的 JSON API", "高：需要路由、搜索索引和构建流程。", "P2", "维护成本上升，且可能偏离备考主线。"),
        ("可交互公式卡片", "把公式、变量、口径、陷阱拆成可翻转卡片和小计算器。", "Quant、FSA、Fixed Income、Derivatives 高频计算复习。", "module `## 5. 关键公式与计算框架`、错题事件。", "中高：需要公式结构化抽取和输入校验。", "P2", "公式卡不能替代题干判断，避免机械刷卡。"),
        ("错题驱动知识图谱", "用错题事件连接 topic、LOS、error_type、fix_rule 和 MOC 节点。", "定位重复犯错、生成 mock 前高风险提醒。", ".system/events、.system/memory/patterns、MOC 节点编号。", "高：需要稳定 taxonomy 和图数据库/JSON 图。", "P1.5", "同义词会造成图谱碎裂，需要 Topic alias 治理。"),
        ("Agent 复盘/提醒/校验界面", "让 agent 基于事件证据生成 brief、retro、validation checklist。", "mock 前后、错题批量复盘、agent 输出审计。", ".system/app workflows、skills、.system/memory/validation。", "中：已有 CLI，可先做薄 UI 或命令面板。", "P2", "不能让 agent 跳过事件层直接给策略。"),
        ("Spaced repetition 与 quiz 模式", "把术语、公式、陷阱、错题 fix rule 转成间隔复习卡和小测。", "考前冲刺、碎片时间、薄弱 LOS 反复练。", "module section 3/5/7、question-errors、patterns。", "中：需要卡片生成、复习状态和淘汰机制。", "P2", "卡片过多会稀释重点，必须按决策价值治理。"),
    ]
    rows = ["| 形态 | 目标 | 适用场景 | 数据源 | 实现门槛 | 优先级 | 风险 |", "|---|---|---|---|---|---|---|"]
    for row in directions:
        rows.append("| " + " | ".join(row) + " |")
    return f"""---
title: "CFA Knowledge Base Display Evolution"
description: "CFA Level I 知识库从 Markdown 稳态展示到 Canvas、Dashboard、Web、知识图谱与 Agent 系统的演进路线"
note_type: strategy
status: active
updated: 2026-05-26
---

# CFA Knowledge Base Display Evolution

> 当前阶段仍以 Markdown 稳态为主。本文只记录未来展示形态的可能性、边界和风险，不把任何未来界面提前写成 source of truth。

## 1. 当前 Markdown 稳态层

- **目标**：让 `CFA_tier1/` 的 10 科 MOC 和 93 个 module 成为可阅读、可链接、可复习的 Obsidian 投影视图。
- **边界**：Markdown 是展示层，不是主存储；官方 module 名称、顺序、LOS 和权重来自 registry。
- **Source of truth**：
  1. `.system/events/` 与 `.system/events/catalog.sqlite3`
  2. `.system/memory/`
  3. 官方 registry：`.system/memory/strategy/cfa-2026-official-module-registry.json`
  4. `CFA_tier1/` Markdown 投影视图
- **当前不做**：不引入 CSS snippet、HTML grid、复杂 Web app 或手工 Canvas 维护。

## 2. 可升级展示形态

{chr(10).join(rows)}

## 3. 数据源与架构边界

- **Capture Layer**：`.system/events/` 捕获错题、偏差和 agent 失误，是动态学习证据。
- **Memory Layer**：`.system/memory/` 沉淀长期资产、pattern、strategy 和 validation。
- **Decision Layer**：`.system/app/` 与 `skills/` 生成复盘、策略和校验。
- **Projection Layer**：`CFA_tier1/`、Dashboard、Canvas、Web app 都只是投影。
- 任何新展示形态都必须能回溯到 registry、事件或 memory，不能手工创造无法验证的结论。

## 4. 推荐演进路线

1. **P1：稳定 Markdown + Dataview 聚合**。先让 frontmatter、module 编号和 MOC 节点稳定，生成 dashboard。
2. **P1.5：错题驱动知识图谱原型**。以 topic alias、LOS、error_type、moc_target 为节点，验证是否真的改善复盘。
3. **P2：公式卡片与 quiz**。只从高频计算模块和重复错题生成，避免卡片泛滥。
4. **P2：Agent brief UI**。在 CLI 工作流稳定后，再做薄界面展示 pre-mock brief、post-mock retro 和 validation。
5. **P3：本地 Web app**。只有当 Markdown + dashboard 已无法支撑检索和交互时再启动。

## 5. 不建议立即做的方向

- **大型 Web app 重写**：会把注意力从备考内容治理转移到界面工程。
- **手工 Canvas 大图**：短期漂亮，但难以复跑，容易和 registry 脱节。
- **全自动 agent 改 MOC**：必须经过 `moc-gap-review`，不能让 pattern mining 直接改 Projection 层。
- **无筛选的卡片化**：所有段落都做成 flashcard 会制造噪音，违背“只沉淀能改变决策的内容”。

## 6. 下一步候选项目

- 为 93 个 module 的编号知识树生成稳定 node id，例如 `QM.M10.10.2`。
- 建立 topic alias taxonomy，减少同义词导致的 pattern 碎裂。
- 从 `.system/events/catalog.sqlite3` 生成 `CFA_tier1/dashboard/Topic弱点页.md`。
- 为高频计算模块抽取公式 JSON，用于未来公式卡片和 quiz。
- 设计 `moc_target` 自动建议规则，把错题更稳定地挂回 MOC 节点。
"""


def update_all() -> None:
    registry = json.loads(read_text(REGISTRY_PATH))
    matches_by_module = build_legacy_matches(registry)

    for subject, subject_data in registry["subjects"].items():
        subject_dir = ROOT / "CFA_tier1" / subject_data["directory"]
        for module in subject_data["modules"]:
            path = subject_dir / module["filename"]
            if path.exists():
                _frontmatter, _body = split_frontmatter(read_text(path))
            rendered = render_module(subject, subject_data, module, matches_by_module.get((subject, module["module"]), []))
            write_text(path, rendered)

        moc_path = moc_filename(subject_dir, subject)
        if moc_path.exists():
            _frontmatter, _body = split_frontmatter(read_text(moc_path))
        write_text(moc_path, render_moc(subject, subject_data, matches_by_module))

    write_text(LEGACY_MAP_PATH, render_legacy_map(registry, matches_by_module))
    write_text(ROADMAP_PATH, render_roadmap())

    module_count = sum(len(subject_data["modules"]) for subject_data in registry["subjects"].values())
    los_count = sum(len(module.get("los", [])) for subject_data in registry["subjects"].values() for module in subject_data["modules"])
    print(f"Updated {len(registry['subjects'])} MOCs and {module_count} modules.")
    print(f"Registry check: {module_count} modules / {los_count} LOS.")
    print(f"Wrote {LEGACY_MAP_PATH.relative_to(ROOT)}")
    print(f"Wrote {ROADMAP_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    update_all()
