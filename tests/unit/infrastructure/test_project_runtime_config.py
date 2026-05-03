import json
from pathlib import Path


def test_project_runtime_uses_common_configuration_without_dev_prod_duplication():
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))

    runtime = project["runtime"]

    assert "common" in runtime
    assert runtime["dev"] == {}
    assert runtime["prod"] == {}


def test_project_runtime_uses_model_identifiers_not_model_paths():
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))

    runtime_common = project["runtime"]["common"]

    assert "AGE_MODEL_ID" in runtime_common
    assert "FACE_DETECTION_MODEL_ID" in runtime_common
    assert "AGE_MODEL_PATH" not in runtime_common
    assert "FACE_DETECTION_MODEL_PATH" not in runtime_common


def test_project_runtime_does_not_expose_threshold_policy_as_runtime_config():
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))

    runtime_text = json.dumps(project["runtime"])

    assert "AGE_THRESHOLD" not in runtime_text
    assert "AGE_MARGIN" not in runtime_text
    assert "CONFIDENCE_THRESHOLD" not in runtime_text
    assert "SIGNAL_QUALITY_THRESHOLD" not in runtime_text
    assert "DEFAULT_AGE_CONFIDENCE" not in runtime_text
