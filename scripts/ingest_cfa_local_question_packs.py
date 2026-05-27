from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


REPO_ROOT = Path(__file__).resolve().parent.parent
VAULT_ROOT = REPO_ROOT / "CFA_tier1"

PRACTICE_PDF = Path(r"D:\3\CFA一级（及时转存，避免丢失）\2026年备考CFA一级Pack1000练习题\CFA L1 付费1000题.pdf")
PRACTICE_ANSWER_DIR = Path(r"D:\3\CFA一级（及时转存，避免丢失）\2026年备考CFA一级Pack1000练习题\1000题答案")
MOCK_DIR = Path(r"D:\3\CFA一级（及时转存，避免丢失）\2026年备考CFA一级Mock5套及答案")

QUESTION_SPLIT_RE = re.compile(r"(?=(?<![,\d])(\d{1,3})\.\s+[A-Z])")
QUESTION_START_TEMPLATE = r"(?<![,\d]){q}\.\s+[A-Z]"
QUESTION_START_RE = re.compile(r"(?<![,\d])(\d{1,3})\.\s+[A-Z]")


@dataclass(frozen=True)
class SubjectSpec:
    key: str
    display: str
    directory: str
    practice_file: str
    mock_bucket: str
    practice_pages: tuple[int, int]
    practice_count: int
    answer_pdf: str


SUBJECTS: list[SubjectSpec] = [
    SubjectSpec(
        key="FRA",
        display="Financial Statement Analysis",
        directory="Financial_Statement_Analysis",
        practice_file="00-Financial-Statement-Analysis-Practice-Questions.md",
        mock_bucket="FRA",
        practice_pages=(1, 29),
        practice_count=130,
        answer_pdf="财务报表.pdf",
    ),
    SubjectSpec(
        key="CorpIss",
        display="Corporate Issuers",
        directory="Corporate_Issuers",
        practice_file="00-Corporate-Issuers-Practice-Questions.md",
        mock_bucket="CorpIss",
        practice_pages=(30, 40),
        practice_count=67,
        answer_pdf="公司金融.pdf",
    ),
    SubjectSpec(
        key="Equity",
        display="Equity",
        directory="Equity",
        practice_file="00-Equity-Practice-Questions.md",
        mock_bucket="Equity",
        practice_pages=(41, 68),
        practice_count=154,
        answer_pdf="股权投资.pdf",
    ),
    SubjectSpec(
        key="FI",
        display="Fixed Income",
        directory="Fixed_Income",
        practice_file="00-Fixed-Income-Practice-Questions.md",
        mock_bucket="FI",
        practice_pages=(69, 90),
        practice_count=106,
        answer_pdf="固定收益.pdf",
    ),
    SubjectSpec(
        key="Economics",
        display="Economics",
        directory="Economics",
        practice_file="00-Economics-Practice-Questions.md",
        mock_bucket="Economics",
        practice_pages=(91, 103),
        practice_count=76,
        answer_pdf="经济学.pdf",
    ),
    SubjectSpec(
        key="AltInv",
        display="Alternative Investments",
        directory="Alternative_Investments",
        practice_file="00-Alternative-Investments-Practice-Questions.md",
        mock_bucket="AltInv",
        practice_pages=(104, 114),
        practice_count=61,
        answer_pdf="另类投资.pdf",
    ),
    SubjectSpec(
        key="Quant",
        display="Quantitative Methods",
        directory="Quantitative_Methods",
        practice_file="00-Quant-Practice-Questions.md",
        mock_bucket="Quant",
        practice_pages=(115, 133),
        practice_count=93,
        answer_pdf="数量分析.pdf",
    ),
    SubjectSpec(
        key="Derivatives",
        display="Derivatives",
        directory="Derivatives",
        practice_file="00-Derivatives-Practice-Questions.md",
        mock_bucket="Derivatives",
        practice_pages=(134, 146),
        practice_count=65,
        answer_pdf="衍生品.pdf",
    ),
    SubjectSpec(
        key="Ethics",
        display="Ethical and Professional Standards",
        directory="Ethical_and_Professional_Standards",
        practice_file="00-Ethics-Practice-Questions.md",
        mock_bucket="Ethics",
        practice_pages=(147, 183),
        practice_count=148,
        answer_pdf="职业道德.pdf",
    ),
    SubjectSpec(
        key="Portfolio",
        display="Portfolio Management",
        directory="Portfolio_Management",
        practice_file="00-Portfolio-Practice-Questions.md",
        mock_bucket="Portfolio",
        practice_pages=(184, 202),
        practice_count=100,
        answer_pdf="组合管理.pdf",
    ),
]

MOCK_BUCKET_ORDER = [spec.mock_bucket for spec in SUBJECTS if spec.mock_bucket == "Ethics"] + [
    "Quant",
    "Economics",
    "FRA",
    "CorpIss",
    "Equity",
    "FI",
    "Derivatives",
    "AltInv",
    "Portfolio",
]

MOCK_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Ethics": (
        "standard",
        "standards",
        "cfa institute",
        "member",
        "candidate",
        "client",
        "supervisor",
        "soft dollar",
        "independence and objectivity",
        "material nonpublic",
        "performance presentation",
        "preservation of confidentiality",
        "loyalty, prudence, and care",
        "gips",
        "misconduct",
        "fair dealing",
        "knowledge of the law",
    ),
    "Quant": (
        "confidence interval",
        "sampling",
        "hypothesis",
        "standard deviation",
        "correlation",
        "covariance",
        "regression",
        "bootstrap",
        "bayes",
        "probability",
        "geometric mean",
        "money-weighted",
        "time-weighted",
        "kurtosis",
        "skewness",
        "semideviation",
        "t-stat",
        "chi-square",
        "simple linear regression",
        "residual",
        "predicted value",
        "machine learning",
        "overfitting",
        "fintech",
        "probability tree",
    ),
    "Economics": (
        "fiscal policy",
        "monetary policy",
        "gdp",
        "inflation",
        "unemployment",
        "exchange rate",
        "central bank",
        "business cycle",
        "oligopoly",
        "tariff",
        "geopolitical",
        "quantitative easing",
        "liquidity trap",
        "central bank",
        "automatic stabilizer",
        "supply curve",
        "price elasticity",
        "business cycle",
    ),
    "FRA": (
        "inventory",
        "financial statement",
        "revenue recognition",
        "impairment",
        "deferred tax",
        "goodwill",
        "pp&e",
        "lease",
        "diluted eps",
        "cash flow",
        "receivable",
        "lifo",
        "fifo",
        "ifrs",
        "u.s. gaap",
        "eps",
        "dilutive",
        "auditor",
        "revaluation model",
        "intangible asset",
        "gross profit margin",
        "write-down",
        "roe",
    ),
    "CorpIss": (
        "wacc",
        "capital budgeting",
        "working capital",
        "dividend",
        "share repurchase",
        "modigliani",
        "pecking order",
        "corporate governance",
        "project",
        "npv",
        "irr",
        "cost of capital",
        "capital structure",
        "real option",
        "board of directors",
        "directors",
        "life-cycle stage",
        "cost of debt",
    ),
    "Equity": (
        "price to earnings",
        "p/e",
        "dividend discount",
        "residual income",
        "free cash flow to equity",
        "free cash flow to the firm",
        "market efficiency",
        "industry",
        "stock",
        "equity market",
        "gordon growth",
        "justified",
        "valuation model",
    ),
    "FI": (
        "bond",
        "yield curve",
        "duration",
        "convexity",
        "spot rate",
        "forward rate",
        "callable",
        "putable",
        "credit spread",
        "mortgage-backed",
        "securitization",
        "float rate",
        "z-spread",
        "credit analysis",
    ),
    "Derivatives": (
        "futures",
        "forward contract",
        "forward price",
        "option",
        "swap",
        "put-call parity",
        "underlying",
        "exercise price",
        "margin",
        "contract",
    ),
    "AltInv": (
        "hedge fund",
        "private equity",
        "real estate",
        "infrastructure",
        "commodity",
        "blockchain",
        "digital asset",
        "farmland",
        "timberland",
        "alternative investment",
        "token",
    ),
    "Portfolio": (
        "investment policy statement",
        "ips",
        "risk tolerance",
        "capital market theory",
        "cal",
        "cml",
        "sml",
        "treynor",
        "sharpe",
        "jensen",
        "value at risk",
        "var",
        "pension",
        "endowment",
        "strategic asset allocation",
        "liquidity requirement",
        "enterprise risk",
        "security market line",
        "capital allocation line",
        "capital market line",
        "smart beta",
        "asset class",
    ),
}


def read_pdf_pages(path: Path) -> list[str]:
    reader = PdfReader(str(path))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"^\d+\s+", "", text)
        pages.append(text)
    return pages


def clean_stem(stem: str) -> str:
    stem = re.sub(r"\s+", " ", stem).strip()
    stem = re.sub(r"^\d+\.\s*", "", stem)
    return stem


def extract_candidates(page_text: str) -> list[tuple[int, str]]:
    parts = QUESTION_SPLIT_RE.split(page_text)
    items: list[tuple[int, str]] = []
    for idx in range(1, len(parts), 2):
        qnum = int(parts[idx])
        body = parts[idx + 1]
        option_match = re.search(r"\sA\.\s", body)
        if not option_match:
            continue
        stem = clean_stem(body[: option_match.start()])
        if len(stem) < 15:
            continue
        items.append((qnum, stem))
    return items


def recover_missing_question(page_text: str, qnum: int) -> str | None:
    start_re = re.compile(QUESTION_START_TEMPLATE.format(q=qnum))
    start_match = start_re.search(page_text)
    if not start_match:
        return None

    next_match = None
    for match in QUESTION_START_RE.finditer(page_text, start_match.end()):
        next_match = match
        break

    body = page_text[start_match.start() : next_match.start() if next_match else len(page_text)]
    option_match = re.search(r"\sA\.\s", body)
    if not option_match:
        return None

    stem = clean_stem(body[: option_match.start()])
    return stem if len(stem) >= 15 else None


def extract_subject_questions(pages: list[str], spec: SubjectSpec) -> list[tuple[int, int, str]]:
    start_page, end_page = spec.practice_pages
    collected: dict[int, tuple[int, str]] = {}
    for page_number in range(start_page, end_page + 1):
        page_text = pages[page_number - 1]
        for qnum, stem in extract_candidates(page_text):
            if 1 <= qnum <= spec.practice_count and qnum not in collected:
                collected[qnum] = (page_number, stem)

    for qnum in range(1, spec.practice_count + 1):
        if qnum in collected:
            continue
        for page_number in range(start_page, end_page + 1):
            page_text = pages[page_number - 1]
            stem = recover_missing_question(page_text, qnum)
            if stem:
                collected[qnum] = (page_number, stem)
                break

    return [(qnum, collected[qnum][0], collected[qnum][1]) for qnum in sorted(collected)]


def classify_mock_question(stem: str) -> tuple[str, int]:
    stem_lower = stem.lower()
    scores: dict[str, int] = {}
    for bucket, keywords in MOCK_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in stem_lower)
        if score:
            scores[bucket] = score
    if not scores:
        return "Unknown", 0
    bucket, score = max(scores.items(), key=lambda item: item[1])
    return bucket, score


def extract_mock_questions(path: Path) -> list[dict[str, object]]:
    pages = read_pdf_pages(path)
    questions: dict[int, tuple[int, str]] = {}
    for page_number, page_text in enumerate(pages, start=1):
        for qnum, stem in extract_candidates(page_text):
            if 1 <= qnum <= 90 and qnum not in questions:
                questions[qnum] = (page_number, stem)
    for qnum in range(1, 91):
        if qnum in questions:
            continue
        for page_number, page_text in enumerate(pages, start=1):
            stem = recover_missing_question(page_text, qnum)
            if stem:
                questions[qnum] = (page_number, stem)
                break

    items: list[dict[str, object]] = []
    for qnum in sorted(questions):
        page_number, stem = questions[qnum]
        bucket, score = classify_mock_question(stem)
        items.append(
            {
                "question_number": qnum,
                "page_number": page_number,
                "stem": stem,
                "bucket": bucket,
                "score": score,
                "mock_name": path.stem,
            }
        )
    return items


def write_markdown(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(lines).rstrip() + "\n"
    body = body.encode("utf-8", "ignore").decode("utf-8", "ignore")
    path.write_text(body, encoding="utf-8")


def build_practice_markdown(spec: SubjectSpec, questions: list[tuple[int, int, str]]) -> list[str]:
    answer_path = PRACTICE_ANSWER_DIR / spec.answer_pdf
    lines = [
        "---",
        f'title: "{spec.display} Practice Questions"',
        'source_type: "local_question_pack"',
        f'source_pdf: "{PRACTICE_PDF}"',
        f'answer_pdf: "{answer_path}"',
        f"question_count: {spec.practice_count}",
        f"source_pages: {spec.practice_pages[0]}-{spec.practice_pages[1]}",
        "---",
        "",
        f"# {spec.display} Practice Questions",
        "",
        f"- Source question pack: `{PRACTICE_PDF}`",
        f"- Source answer pack: `{answer_path}`",
        f"- Question count target: {spec.practice_count}",
        f"- Extracted question stems: {len(questions)}",
        "",
        "## Questions",
    ]
    for qnum, page_number, stem in questions:
        lines.append(f"- Q{qnum:03d} | p.{page_number} | {stem}")
    return lines


def build_subject_bank_dashboard(practice_links: list[tuple[SubjectSpec, int]]) -> list[str]:
    lines = [
        "---",
        'title: "CFA L1 Subject Question Banks"',
        'description: 本地基础题与题库承接页索引',
        "generated: 2026-05-27",
        f'source: "{PRACTICE_PDF.parent}"',
        "---",
        "",
        "# CFA L1 Subject Question Banks",
        "",
        "> 本页汇总本地 Pack1000 基础题承接页。题干来自本地 PDF，答案解析保持对源 PDF 的引用，不把整份答案全文写进仓库。",
        "",
        "## 基础题概览",
        "",
        "| 科目 | 基础题数 | 题库文件 |",
        "|------|----------|----------|",
    ]
    for spec, extracted_count in practice_links:
        wiki = Path(spec.practice_file).stem
        lines.append(f"| {spec.display} | {spec.practice_count} | [[{wiki}]] |")

    lines.extend(
        [
            "",
            "## 说明",
            "",
            "- `基础题数` 以对应答案 PDF 的题号容量为准。",
            "- 各科题库页记录题号、题干摘要和源页码，便于后续把高频题型回填到 MOC 或 drill。",
            "- 若后续要把某题升级为错题事件，请再走 `record-mistake`，不要直接把基础题索引当成个人错题本。",
        ]
    )
    return lines


def build_mock_index(mock_items: list[dict[str, object]]) -> list[str]:
    grouped: dict[str, int] = {}
    for item in mock_items:
        grouped[item["bucket"]] = grouped.get(item["bucket"], 0) + 1

    lines = [
        "---",
        'title: "Mock Source Index"',
        'source_type: "local_mock_pack"',
        f'source_root: "{MOCK_DIR}"',
        "---",
        "",
        "# Mock Source Index",
        "",
        f"- Source root: `{MOCK_DIR}`",
        f"- Parsed mock papers: {len({item['mock_name'] for item in mock_items})}",
        f"- Parsed mock questions: {len(mock_items)}",
        "",
        "## Bucket Counts",
    ]
    for bucket in MOCK_BUCKET_ORDER:
        lines.append(f"- {bucket}: {grouped.get(bucket, 0)}")
    lines.append(f"- Unknown: {grouped.get('Unknown', 0)}")
    return lines


def build_mock_bucket_markdown(spec: SubjectSpec, items: list[dict[str, object]]) -> list[str]:
    lines = [
        "---",
        f"bucket: {spec.mock_bucket}",
        f"question_count: {len(items)}",
        f'source_root: "{MOCK_DIR}"',
        "---",
        "",
        f"# {spec.display} Mock Questions",
        "",
        "- 这里记录的是本地 mock 题源，不是个人错题事件。",
        "- 科目归类以题干关键词和题目顺序做启发式划分，后续可继续校正。",
        "",
        "## Questions",
    ]
    for item in items:
        lines.append(
            f"- {item['mock_name']} Q{item['question_number']:02d} | p.{item['page_number']} | {item['stem']}"
        )
    return lines


def build_mock_unknown_markdown(items: list[dict[str, object]]) -> list[str]:
    lines = [
        "---",
        f"question_count: {len(items)}",
        f'source_root: "{MOCK_DIR}"',
        "---",
        "",
        "# Mock Unclassified Questions",
        "",
        "- 这些题目暂时没被高置信地映射到单一科目。",
        "- 保留原题干和源页码，后续可以继续细分到具体科目页。",
        "",
        "## Questions",
    ]
    for item in items:
        lines.append(
            f"- {item['mock_name']} Q{item['question_number']:02d} | p.{item['page_number']} | {item['stem']}"
        )
    return lines


def main() -> None:
    practice_pages = read_pdf_pages(PRACTICE_PDF)
    practice_links: list[tuple[SubjectSpec, int]] = []
    for spec in SUBJECTS:
        questions = extract_subject_questions(practice_pages, spec)
        target = VAULT_ROOT / spec.directory / spec.practice_file
        write_markdown(target, build_practice_markdown(spec, questions))
        practice_links.append((spec, len(questions)))

    dashboard_path = VAULT_ROOT / "dashboard" / "Subject-Question-Banks.md"
    write_markdown(dashboard_path, build_subject_bank_dashboard(practice_links))

    mock_files = sorted(MOCK_DIR.glob("CFA L1 *.pdf"))
    all_mock_items: list[dict[str, object]] = []
    bucketed: dict[str, list[dict[str, object]]] = {spec.mock_bucket: [] for spec in SUBJECTS}
    for mock_file in mock_files:
        if mock_file.name.startswith("模考答案"):
            continue
        for item in extract_mock_questions(mock_file):
            all_mock_items.append(item)
            bucketed.setdefault(str(item["bucket"]), []).append(item)

    mock_index_path = VAULT_ROOT / "mock" / "00-Mock-Source-Index.md"
    write_markdown(mock_index_path, build_mock_index(all_mock_items))

    for spec in SUBJECTS:
        target = VAULT_ROOT / "mock" / spec.mock_bucket / f"00-{spec.mock_bucket}-Mock-Questions.md"
        items = sorted(
            bucketed.get(spec.mock_bucket, []),
            key=lambda item: (str(item["mock_name"]), int(item["question_number"])),
        )
        write_markdown(target, build_mock_bucket_markdown(spec, items))

    unknown_items = sorted(
        bucketed.get("Unknown", []),
        key=lambda item: (str(item["mock_name"]), int(item["question_number"])),
    )
    unknown_target = VAULT_ROOT / "mock" / "00-Mock-Unclassified.md"
    write_markdown(unknown_target, build_mock_unknown_markdown(unknown_items))


if __name__ == "__main__":
    main()
