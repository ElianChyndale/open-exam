from language_science.interleaving import InterleavingBuilderV2, InterleavingConfigV2, CFA_ADJACENCY, LANGUAGE_ADJACENCY


def test_cfa_adjacency_has_entries():
    assert len(CFA_ADJACENCY) >= 15, "CFA adjacency map must have at least 15 entries"


def test_language_adjacency_has_entries():
    assert len(LANGUAGE_ADJACENCY) >= 8, "Language adjacency map must have at least 8 entries"


def test_find_adjacent_cfa():
    builder = InterleavingBuilderV2(domain="cfa")
    related = builder.find_adjacent("NPV")
    assert "IRR" in related


def test_find_adjacent_language():
    builder = InterleavingBuilderV2(domain="language")
    related = builder.find_adjacent("its")
    assert len(related) > 0


def test_interleaving_build_basic():
    builder = InterleavingBuilderV2(domain="cfa")
    weak = [{"item_id": "1", "canonical_form": "NPV"}, {"item_id": "2", "canonical_form": "Duration"}]
    old = [{"item_id": "3", "canonical_form": "LIFO"}]
    maintenance = [{"item_id": "4", "canonical_form": "DCF"}]
    result = builder.build(weak, old, maintenance)
    assert len(result.items) >= 2


def test_interleaving_composition():
    builder = InterleavingBuilderV2(domain="cfa")
    weak = [{"item_id": str(i), "canonical_form": f"term-{i}"} for i in range(20)]
    old = [{"item_id": str(i), "canonical_form": f"old-{i}"} for i in range(10)]
    maintenance = [{"item_id": str(i), "canonical_form": f"maint-{i}"} for i in range(10)]
    new_items = [{"item_id": str(i), "canonical_form": f"new-{i}"} for i in range(10)]
    config = InterleavingConfigV2(max_items=20)
    result = builder.build(weak, old, maintenance, new_items, config)
    assert result.composition["weak"] > 0
    assert result.composition["maintenance"] > 0


def test_retrieval_prompts():
    from study_science.retrieval import format_retrieval_prompt, score_recall
    prompt = format_retrieval_prompt("definition", "NPV", related="IRR")
    assert "NPV" in prompt
    result = score_recall("net present value", "net present value of future cash flows")
    assert 0 < result["score"] <= 1.0
