import pytest

from app.domain.models.metadata import ModelMetadata
from app.infrastructure.models.registry import StaticModelRegistry


def test_static_model_registry_returns_model_by_identifier():
    model = ModelMetadata(
        model_id="credona.age.test.v1",
        model_version="1.0.0",
        task="age_estimation",
        runtime="onnx",
        path="models/test.onnx",
        scoring_policy_id="credona.age.policy.v1",
    )

    registry = StaticModelRegistry(models={model.model_id: model})

    assert registry.get("credona.age.test.v1") == model


def test_static_model_registry_rejects_unknown_model_identifier():
    model = ModelMetadata(
        model_id="credona.age.test.v1",
        model_version="1.0.0",
        task="age_estimation",
        runtime="onnx",
        path="models/test.onnx",
        scoring_policy_id="credona.age.policy.v1",
    )

    registry = StaticModelRegistry(models={model.model_id: model})

    with pytest.raises(ValueError, match="Unknown model identifier"):
        registry.get("credona.age.unknown.v1")


def test_static_model_registry_rejects_invalid_model_metadata():
    model = ModelMetadata(
        model_id="credona.age.test.v1",
        model_version="1.0.0",
        task="unsupported",
        runtime="onnx",
        path="models/test.onnx",
        scoring_policy_id="credona.age.policy.v1",
    )

    with pytest.raises(ValueError, match="unsupported model task"):
        StaticModelRegistry(models={model.model_id: model})
