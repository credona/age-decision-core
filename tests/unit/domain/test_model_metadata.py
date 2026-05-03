import pytest

from app.domain.models.metadata import ModelMetadata


def test_model_metadata_accepts_valid_model_definition():
    metadata = ModelMetadata(
        model_id="credona.age.test.v1",
        model_version="1.0.0",
        task="age_estimation",
        runtime="onnx",
        path="models/test.onnx",
        scoring_policy_id="credona.age.policy.v1",
    )

    metadata.validate()


def test_model_metadata_rejects_missing_model_id():
    metadata = ModelMetadata(
        model_id="",
        model_version="1.0.0",
        task="age_estimation",
        runtime="onnx",
        path="models/test.onnx",
        scoring_policy_id="credona.age.policy.v1",
    )

    with pytest.raises(ValueError, match="model_id"):
        metadata.validate()


def test_model_metadata_rejects_unsupported_runtime():
    metadata = ModelMetadata(
        model_id="credona.age.test.v1",
        model_version="1.0.0",
        task="age_estimation",
        runtime="pytorch",
        path="models/test.onnx",
        scoring_policy_id="credona.age.policy.v1",
    )

    with pytest.raises(ValueError, match="runtime"):
        metadata.validate()
