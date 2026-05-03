from pathlib import Path


def test_models_doc_uses_model_identifiers_not_paths():
    content = Path("docs/models.md").read_text(encoding="utf-8")

    assert "model_id" in content
    assert "model_version" in content


def test_benchmarks_doc_requires_model_reproducibility():
    content = Path("docs/benchmarks.md").read_text(encoding="utf-8")

    assert "model_id" in content
    assert "scoring_policy_id" in content
