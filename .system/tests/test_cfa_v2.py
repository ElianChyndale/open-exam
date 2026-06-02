from pathlib import Path
from app.cfa_storage import CfaRepository
from app.cfa_workflows import create_cfa_item, create_cfa_card, review_cfa_card, due_cfa_cards, EXAM_WEIGHTS
from app.storage import Repository
from study_science.distractor import DistractorAnalyzer, DISTRACTOR_TYPES


def test_cfa_storage_initial_state(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    state = cfa.replay()
    assert state["items"] == {}
    assert state["cards"] == {}
    assert state["mock_sessions"] == []


def test_create_cfa_item(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    item = create_cfa_item(cfa, item_type="cfa_formula", canonical_form="DCF", topic="Equity")
    assert item["item_id"] in cfa.replay()["items"]


def test_create_cfa_card(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    item = create_cfa_item(cfa, item_type="cfa_formula", canonical_form="WACC", topic="Corporate_Issuers")
    card = create_cfa_card(cfa, item)
    assert card["card_id"] in cfa.replay()["cards"]


def test_cfa_review_card(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    item = create_cfa_item(cfa, item_type="cfa_concept", canonical_form="Duration", topic="Fixed_Income")
    card = create_cfa_card(cfa, item)
    reviewed = review_cfa_card(cfa, card["card_id"], "good")
    assert reviewed["fsrs_state"]["stability"] > 0
    assert reviewed["fsrs_state"]["difficulty"] > 0


def test_exam_weights_sum():
    total = sum(EXAM_WEIGHTS.values())
    assert 0.95 <= total <= 1.05, f"Exam weights should sum to ~1.0, got {total}"


def test_exam_weight_in_scheduling(tmp_path: Path):
    """Higher-weight topics should get lower difficulty adjustment."""
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    ethics_item = create_cfa_item(cfa, item_type="cfa_concept", canonical_form="Standard I", topic="Ethical_and_Professional_Standards")
    deriv_item = create_cfa_item(cfa, item_type="cfa_concept", canonical_form="Forward", topic="Derivatives")
    ethics_card = create_cfa_card(cfa, ethics_item)
    deriv_card = create_cfa_card(cfa, deriv_item)
    assert ethics_card["exam_weight"] > deriv_card["exam_weight"]


def test_distractor_analyzer():
    da = DistractorAnalyzer()
    da.record_attempt("item-1", False, "inverse_relationship", "Fixed_Income")
    da.record_attempt("item-1", False, "inverse_relationship", "Fixed_Income")
    da.record_attempt("item-1", True, "", "Fixed_Income")
    assert len(da.get_patterns("item-1")) == 3
    assert da.most_common_distractor("Fixed_Income") == "inverse_relationship"


def test_due_cfa_cards_respects_weights(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    ethics = create_cfa_item(cfa, item_type="cfa_concept", canonical_form="Ethics", topic="Ethical_and_Professional_Standards")
    derivs = create_cfa_item(cfa, item_type="cfa_concept", canonical_form="Deriv", topic="Derivatives")
    create_cfa_card(cfa, ethics)
    create_cfa_card(cfa, derivs)
    due = due_cfa_cards(cfa)
    assert len(due) == 2
