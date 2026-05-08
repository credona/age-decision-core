from pathlib import Path


def test_models_doc_uses_model_identifiers_not_paths():
    content = Path("docs/models.md").read_text(encoding="utf-8")

    assert "model_id" in content
    assert "model_version" in content


def test_local_benchmark_documentation_is_not_kept_in_core():
    assert not Path("docs/benchmarks.md").exists()


def test_models_doc_requires_model_reproducibility_metadata():
    content = Path("docs/models.md").read_text(encoding="utf-8")

    assert "model_id" in content
    assert "model_version" in content
