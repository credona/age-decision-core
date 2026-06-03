import numpy as np
import pytest

from app.application.use_cases.decision_pipeline import DecisionPipeline
from app.domain.calibration import CalibrationPolicyMetadata, RuntimeCalibrationPolicy


class FakeInferenceEngine:
    def get_status(self) -> dict:
        return {"engine": "fake-inference"}

    def predict(self, prepared_input: np.ndarray) -> tuple[float, float]:
        return 19.0, 0.9


class FakeInputAnalyzer:
    def get_status(self) -> dict:
        return {"engine": "fake-analyzer"}

    def detect(self, image: np.ndarray) -> list:
        return [{"x": 0, "y": 0, "width": 10, "height": 10}]


class FakeImageDecoder:
    def decode(self, image_bytes: bytes) -> np.ndarray:
        return np.zeros((10, 10, 3), dtype=np.uint8)


class FakeFaceCropper:
    def crop(self, image: np.ndarray, faces: list) -> np.ndarray:
        return image


class FakeInputPreprocessor:
    def preprocess(self, face_image: np.ndarray) -> np.ndarray:
        return np.zeros((1, 224, 224, 3), dtype=np.float32)


def make_policy(decision_offset: float) -> RuntimeCalibrationPolicy:
    return RuntimeCalibrationPolicy(
        metadata=CalibrationPolicyMetadata(
            policy_id=f"core-policy-offset-{decision_offset}",
            service="core",
            contract_version="2.6",
            policy_version="1.0.0",
            benchmark_attestation_id="benchmark-attestation-test",
            model_identifier="credona.age.age-gender-onnx.v1",
            payload_hash="sha256:test",
            signature="signature-test",
        ),
        private_payload={
            "calibration_parameters": {
                "decision_offset": decision_offset,
                "signal_quality_offset": 0.0,
            }
        },
    )


def make_pipeline(runtime_calibration: RuntimeCalibrationPolicy | None = None) -> DecisionPipeline:
    return DecisionPipeline(
        inference_engine=FakeInferenceEngine(),
        input_analyzer=FakeInputAnalyzer(),
        image_decoder=FakeImageDecoder(),
        face_cropper=FakeFaceCropper(),
        input_preprocessor=FakeInputPreprocessor(),
        runtime_calibration=runtime_calibration,
    )


async def run_pipeline(pipeline: DecisionPipeline) -> dict:
    return await pipeline.run(
        image_bytes=b"fake-image",
        content_type="image/jpeg",
        request_id="req-test",
        correlation_id="corr-test",
        age_threshold=18,
        majority_country=None,
    )


@pytest.mark.anyio
async def test_runtime_calibration_changes_public_decision() -> None:
    neutral_response = await run_pipeline(make_pipeline())
    calibrated_response = await run_pipeline(make_pipeline(make_policy(decision_offset=3.0)))

    assert neutral_response["decision"] == "uncertain"
    assert calibrated_response["decision"] == "match"

    assert neutral_response["cred_decision_score"] != calibrated_response["cred_decision_score"]

    serialized = str(calibrated_response)

    assert "decision_offset" not in serialized
    assert "calibration_parameters" not in serialized
    assert "private_payload" not in serialized
