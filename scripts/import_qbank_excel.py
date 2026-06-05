#!/usr/bin/env python3
"""
题库批量导入脚本 — 从 Excel/CSV 导入题目到 Question Bank。

用法:
  python scripts/import_qbank_excel.py <文件.xlsx/.csv> [选项]

选项:
  --exam <考试名称>        默认自动检测或 "CFA Level I"
  --source <来源标签>      文件来源名，默认用文件名
  --dry-run                只验证不写入
  --api                   通过 API 导入（需要服务运行中），否则直接写入文件

Excel/CSV 列名映射（支持中英文）:
  exam / 考试
  subject / 科目
  chapter / 章节
  prompt / 题干 / 题目
  choices / 选项（分号分隔，或用独立列 A、B、C、D）
  answer / 答案 / 正确答案
  explanation / 解析 / 解答
  difficulty / 难度
  knowledge_tags / 标签 / 知识点（分号分隔）
  topic / 主题
  module / 模块
  los / 学习成果
"""

import csv
import json
import sys
import argparse
from pathlib import Path
from typing import Any

# ── 列名映射 ──
COLUMN_ALIASES: dict[str, list[str]] = {
    "exam": ["exam", "考试", "考试项目", "exam_project"],
    "subject": ["subject", "科目", "学科"],
    "chapter": ["chapter", "章节", "章"],
    "prompt": ["prompt", "题干", "题目", "question", "stem"],
    "choices": ["choices", "选项", "options"],
    "answer": ["answer", "答案", "正确答案", "correct_answer"],
    "explanation": ["explanation", "解析", "解答", "rationale", "solution"],
    "difficulty": ["difficulty", "难度"],
    "knowledge_tags": ["knowledge_tags", "tags", "标签", "知识点", "知识标签", "knowledge_point"],
    "topic": ["topic", "主题"],
    "module": ["module", "模块"],
    "los": ["los", "learning_outcome", "学习成果"],
    "question_type": ["question_type", "题型", "type"],
}


def resolve_column(headers: list[str]) -> dict[str, str]:
    """Match actual column headers to canonical field names."""
    header_lower = {h.strip().lower(): h.strip() for h in headers}
    mapping: dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias.lower() in header_lower:
                mapping[canonical] = header_lower[alias.lower()]
                break
    return mapping


def parse_choices(cell_value: str) -> list[str]:
    """Parse choices from a cell. Supports semicolon, newline, or pipe delimiters."""
    if not cell_value or not cell_value.strip():
        return []
    text = cell_value.strip()
    if ";" in text:
        return [c.strip() for c in text.split(";") if c.strip()]
    if "|" in text:
        return [c.strip() for c in text.split("|") if c.strip()]
    if "\n" in text:
        return [c.strip() for c in text.split("\n") if c.strip()]
    return [text]


def try_extract_choice_columns(headers: list[str], row: dict[str, Any]) -> list[str] | None:
    """If no 'choices' column, try A/B/C/D or 选项A/选项B/... columns."""
    choice_headers = [h for h in headers if h.strip().upper() in {"A", "B", "C", "D", "E", "F"}]
    if not choice_headers:
        choice_headers = [h for h in headers if h.strip().startswith("选项") or h.strip().startswith("choice")]
    if not choice_headers:
        return None
    return [row.get(h, "") for h in sorted(choice_headers, key=lambda x: x.strip().upper()) if row.get(h, "").strip()]


def resolve_exam(exam_value: str | None, filename: str) -> str:
    """Auto-detect exam from file name if not specified."""
    if exam_value and exam_value.strip():
        return exam_value.strip()
    name_lower = Path(filename).stem.lower()
    if "cfa" in name_lower:
        if "l1" in name_lower or "level1" in name_lower or "level_1" in name_lower:
            return "CFA Level I"
        if "l2" in name_lower:
            return "CFA Level II"
        return "CFA Level I"
    if "frm" in name_lower:
        if "p1" in name_lower:
            return "FRM Part I"
        return "FRM Part I"
    return "CFA Level I"


def row_to_question(row: dict[str, Any], mapping: dict[str, str], filename: str) -> dict[str, Any]:
    """Convert a CSV/Excel row to a question dict matching the API format."""
    q: dict[str, Any] = {}

    exam_field = mapping.get("exam")
    q["exam"] = resolve_exam(row.get(exam_field) if exam_field else None, filename)

    for field, canonical in [
        ("subject", "subject"),
        ("chapter", "chapter"),
        ("topic", "topic"),
        ("module", "module"),
        ("los", "los"),
        ("question_type", "question_type"),
    ]:
        col = mapping.get(field)
        q[canonical] = (row.get(col) or "").strip() if col else ""

    prompt_col = mapping.get("prompt")
    q["prompt"] = (row.get(prompt_col) or "").strip() if prompt_col else ""

    # Choices
    choices_col = mapping.get("choices")
    if choices_col:
        q["choices"] = parse_choices(row.get(choices_col, ""))
    else:
        extracted = try_extract_choice_columns(list(row.keys()), row)
        if extracted:
            q["choices"] = extracted
        else:
            q["choices"] = []

    answer_col = mapping.get("answer")
    q["answer"] = (row.get(answer_col) or "").strip() if answer_col else ""

    explanation_col = mapping.get("explanation")
    q["explanation"] = (row.get(explanation_col) or "").strip() if explanation_col else ""

    difficulty_col = mapping.get("difficulty")
    q["difficulty"] = (row.get(difficulty_col) or "unknown").strip() if difficulty_col else "unknown"

    tags_col = mapping.get("knowledge_tags")
    if tags_col:
        raw_tags = row.get(tags_col, "")
        q["knowledge_tags"] = [t.strip() for t in raw_tags.split(";") if t.strip()] if raw_tags else []
    else:
        q["knowledge_tags"] = []

    return q


def read_csv(path: Path, delimiter: str = ",") -> list[dict[str, Any]]:
    """Read a CSV file."""
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return list(reader)


def read_excel(path: Path) -> list[dict[str, Any]]:
    """Read an Excel file using openpyxl."""
    try:
        import openpyxl
    except ImportError:
        print("ERROR: 需要安装 openpyxl: pip install openpyxl", file=sys.stderr)
        sys.exit(1)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    if ws is None:
        print("ERROR: Excel 文件没有活动工作表", file=sys.stderr)
        sys.exit(1)
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [str(h) if h is not None else "" for h in rows[0]]
    result: list[dict[str, Any]] = []
    for row in rows[1:]:
        if any(cell is not None and str(cell).strip() for cell in row):
            result.append(dict(zip(headers, [str(c) if c is not None else "" for c in row])))
    wb.close()
    return result


def write_questions_direct(questions: list[dict], source_file: str, repo_root: Path) -> dict[str, Any]:
    """Write questions directly to the question bank storage."""
    sys.path.insert(0, str(repo_root / ".system"))
    sys.path.insert(0, str(repo_root / "apps" / "api"))
    from app.question_banks import import_questions
    from app.storage import Repository

    repo = Repository(repo_root)
    return import_questions(repo, source_file, questions)


def import_via_api(questions: list[dict], source_file: str, base_url: str = "http://127.0.0.1:8000") -> dict:
    """Import questions via the REST API."""
    try:
        import httpx
    except ImportError:
        print("ERROR: 需要 httpx: pip install httpx", file=sys.stderr)
        sys.exit(1)

    payload = {"source_file": source_file, "questions": questions}
    resp = httpx.post(f"{base_url}/api/question-banks/import", json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="批量导入题目到 Question Bank")
    parser.add_argument("file", help="Excel (.xlsx) 或 CSV (.csv) 文件路径")
    parser.add_argument("--exam", default="", help="考试名称（默认自动检测）")
    parser.add_argument("--source", default="", help="来源标签（默认用文件名）")
    parser.add_argument("--dry-run", action="store_true", help="只验证不写入")
    parser.add_argument("--api", action="store_true", help="通过 API 导入")
    parser.add_argument("--api-url", default="http://127.0.0.1:8000", help="API 地址")
    parser.add_argument("--delimiter", default=",", help="CSV 分隔符（默认逗号）")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: 文件不存在: {path}", file=sys.stderr)
        sys.exit(1)

    # Read
    ext = path.suffix.lower()
    if ext == ".csv":
        rows = read_csv(path, args.delimiter)
    elif ext in {".xlsx", ".xls"}:
        rows = read_excel(path)
    else:
        print(f"ERROR: 不支持的文件格式: {ext}（支持 .csv / .xlsx）", file=sys.stderr)
        sys.exit(1)

    if not rows:
        print("ERROR: 文件为空或表头无法识别", file=sys.stderr)
        sys.exit(1)

    # Detect columns
    headers = list(rows[0].keys())
    mapping = resolve_column(headers)
    found = list(mapping.keys())
    print(f"📄 文件: {path.name}")
    print(f"📊 行数: {len(rows)}（含表头）")
    print(f"🏷️  识别的列: {', '.join(sorted(found))}")
    missing = [c for c in ["prompt", "choices", "answer"] if c not in mapping]
    if missing:
        print(f"⚠️  缺少必要列: {', '.join(missing)}（将导致导入失败或数据不完整）")

    # Convert
    source_file = args.source or path.name
    questions = []
    errors = []
    for i, row in enumerate(rows, start=2):
        try:
            q = row_to_question(row, mapping, source_file)
            if args.exam:
                q["exam"] = args.exam
            # Basic validation
            issues = []
            if not q.get("prompt"):
                issues.append("题干为空")
            if not q.get("choices") or len(q["choices"]) < 2:
                issues.append("选项不足")
            if not q.get("answer"):
                issues.append("答案为空")
            if issues:
                errors.append((i, issues, q.get("prompt", "")[:50]))
            questions.append(q)
        except Exception as e:
            errors.append((i, [str(e)], ""))

    print(f"✅ 解析成功: {len(questions)} 题")
    if errors:
        print(f"⚠️  解析警告/错误 ({len(errors)} 行):")
        for line, issues, preview in errors[:10]:
            print(f"   行 {line}: {'; '.join(issues)} | {preview}")
        if len(errors) > 10:
            print(f"   ... 还有 {len(errors) - 10} 行")

    if args.dry_run:
        print("\n🏁 Dry-run 模式，未写入任何数据")
        return

    # Import
    if args.api:
        print(f"\n📤 通过 API 导入 ({args.api_url})...")
        result = import_via_api(questions, source_file, args.api_url)
    else:
        print("\n📤 直接写入题库文件...")
        result = write_questions_direct(questions, source_file, Path.cwd())

    print(f"\n📊 导入结果:")
    print(f"   ✅ 已导入: {result.get('imported_count', 0)}")
    print(f"   ✅ 自动验证通过: {result.get('verified_count', 0)}")
    print(f"   ⏳ 待审核: {result.get('quarantined_count', 0)}")
    print(f"   ❌ 拒绝: {result.get('rejected_count', 0)}")
    print(f"   🔁 重复跳过: {result.get('duplicate_count', 0)}")
    print(f"   🔒 锁定拒绝: {result.get('locked_count', 0)}")

    if result.get("rejected"):
        print("\n❌ 拒绝详情:")
        for r in result["rejected"][:5]:
            print(f"   {r.get('question_id')}: {'; '.join(r.get('errors', []))}")


if __name__ == "__main__":
    main()
