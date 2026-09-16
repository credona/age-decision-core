import hashlib

import pytest

from app.domain.models.metadata import ModelMetadata
from app.infrastructure.models.registry import StaticModelRegistry
from app.infrastructure.science.private_model_identity import (
    build_private_scientific_model_identity,
    sha256_file,
)


def model(
    *,
    model_id: str,
    model_version: str,
    task: str,
    path: str,
) -> ModelMetadata:
    return ModelMetadata(
        model_id=model_id,
        model_version=model_version,
        task=task,
        runtime="onnx",
        path=path,
        scoring_policy_id="none",
    )


def test_sha256_file_hashes_exact_bytes(tmp_path) -> None:
    artifact = tmp_path / "model.onnx"
    artifact.write_bytes(b"exact-model-bytes")

    assert sha256_file(artifact) == hashlib.sha256(
        b"exact-model-bytes"
    ).hexdigest()


def test_private_model_identity_hashes_models_without_exposing_paths(
    tmp_path,
) -> None:
    age_path = tmp_path / "age.onnx"
    face_path = tmp_path / "face.onnx"

    age_path.write_bytes(b"age-model")
    face_path.write_bytes(b"face-model")

    age = model(
        model_id="credona.age.test.v1",
        model_version="1.2.3",
        task="age_estimation",
        path="age.onnx",
    )
    face = model(
        model_id="credona.face.test.v1",
        model_version="4.5.6",
        task="face_detection",
        path="face.onnx",
    )

    registry = StaticModelRegistry(
        models={
            face.model_id: face,
            age.model_id: age,
        }
    )

    identity = build_private_scientific_model_identity(
        registry=registry,
        root=tmp_path,
    )

    assert identity == {
        "models": [
            {
                "model_id": "credona.age.test.v1",
                "model_version": "1.2.3",
                "task": "age_estimation",
                "sha256": hashlib.sha256(
                    b"age-model"
                ).hexdigest(),
            },
            {
                "model_id": "credona.face.test.v1",
                "model_version": "4.5.6",
                "task": "face_detection",
                "sha256": hashlib.sha256(
                    b"face-model"
                ).hexdigest(),
            },
        ]
    }

    serialized = str(identity)

    assert "age.onnx" not in serialized
    assert "face.onnx" not in serialized
    assert str(tmp_path) not in serialized


def test_private_model_identity_rejects_missing_artifact(
    tmp_path,
) -> None:
    missing = model(
        model_id="credona.age.missing.v1",
        model_version="1.0.0",
        task="age_estimation",
        path="missing.onnx",
    )

    registry = StaticModelRegistry(
        models={
            missing.model_id: missing,
        }
    )

    with pytest.raises(
        FileNotFoundError,
        match="configured model artifact does not exist",
    ):
        build_private_scientific_model_identity(
            registry=registry,
            root=tmp_path,
        )
