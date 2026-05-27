from pathlib import Path

from scripts.cfa_c_plus_redesign import is_active_knowledge_file, remove_mechanical_sections


def test_is_active_knowledge_file_excludes_legacy_archive_mock_dashboard():
    assert is_active_knowledge_file(Path("CFA_tier1/Quantitative_Methods/M01-Rates-and-Returns.md"))
    assert not is_active_knowledge_file(Path("CFA_tier1/Quantitative_Methods/_legacy/M01-Rates-and-Returns.md"))
    assert not is_active_knowledge_file(Path("CFA_tier1/Economics/_archive/M01-The-Firm-and-Market-Structures.md"))
    assert not is_active_knowledge_file(Path("CFA_tier1/mock/Quant/00-Quant-Mock-Questions.md"))
    assert not is_active_knowledge_file(Path("CFA_tier1/dashboard/Subject-Question-Banks.md"))


def test_remove_mechanical_sections_deletes_previous_patch_blocks():
    source = """# M01

## Textbook Signal Topics

- Textbook volume: `V1`

## 1. 模块定位

Body stays.

### 教材驱动补强（按原版教材回看）

| 教材锚点 | 回看重点 |
|---|---|

## 5. 关键公式与计算框架

Formula stays.

### 教材驱动解题动作

- old action

## 7. 易错点与考试陷阱

Trap stays.

### 教材驱动易错清单

| 易错来源 | 常见误判 |
|---|---|

## 8. 复习安排

End stays.
"""
    cleaned = remove_mechanical_sections(source)
    assert "## Textbook Signal Topics" not in cleaned
    assert "教材驱动补强" not in cleaned
    assert "教材驱动解题动作" not in cleaned
    assert "教材驱动易错清单" not in cleaned
    assert "Body stays." in cleaned
    assert "Formula stays." in cleaned
    assert "Trap stays." in cleaned
    assert "End stays." in cleaned
