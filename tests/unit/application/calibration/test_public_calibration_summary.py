from app.application.calibration.activate_runtime_calibration import (
    ActivateRuntimeCalibrationUseCase,
)
from app.application.calibration.get_public_calibration_summary import (
    GetPublicCalibrationSummaryUseCase,
)
from app.domain.calibration import CalibrationPolicyMetadata, RuntimeCalibrationPolicy
from app.infrastructure.calibration.memory_lifecycle_store import (
    MemoryCalibrationLifecycleStore,
)

FORBIDDEN_PRIVATE_FIELDS = (
    "private_payload",
    "calibration_parameters",
    "decision_offset",
    "signal_quality_offset",
    "payload_hash",
    "signature",
)


def make_policy() -> RuntimeCalibrationPolicy:
    return RuntimeCalibrationPolicy(
        metadata=CalibrationPolicyMetadata(
            policy_id="core-policy-v1",
            service="core",
            contract_version="2.6",
            policy_version="1.0.0",
            benchmark_attestation_id="benchmark-attestation-1",
            model_identifier="credona.age.age-gender-onnx.v1",
            payload_hash="sha256:private",
            signature="private-signature",
        ),
        private_payload={
            "calibration_parameters": {
                "decision_offset": 3.0,
                "signal_quality_offset": 0.1,
            }
        },
    )


def test_public_calibration_summary_returns_none_without_active_policy() -> None:
    store = MemoryCalibrationLifecycleStore()

    assert GetPublicCalibrationSummaryUseCase(store).execute() is None


def test_public_calibration_summary_excludes_private_payload() -> None:
    store = MemoryCalibrationLifecycleStore()
    policy = make_policy()

    ActivateRuntimeCalibrationUseCase(store, store).execute(policy=policy)

    summary = GetPublicCalibrationSummaryUseCase(store).execute()

    assert summary == {
        "policy_id": "core-policy-v1",
        "policy_version": "1.0.0",
        "benchmark_attestation_id": "benchmark-attestation-1",
        "model_identifier": "credona.age.age-gender-onnx.v1",
        "service": "core",
        "contract_version": "2.6",
        "active": True,
    }

    serialized = str(summary)

    for field in FORBIDDEN_PRIVATE_FIELDS:
        assert field not in serialized
