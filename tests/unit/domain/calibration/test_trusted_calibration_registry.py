import pytest

from app.domain.calibration import (
    CalibrationActivationError,
    CalibrationPolicyMetadata,
    RuntimeCalibrationPolicy,
    TrustedCalibrationPolicyRef,
    TrustedCalibrationRegistry,
)


def make_policy(
    *,
    policy_id: str = "core-policy-v1",
    service: str = "core",
    contract_version: str = "2.6",
    model_identifier: str = "credona.age.age-gender-onnx.v1",
    payload_hash: str = "sha256:test",
) -> RuntimeCalibrationPolicy:
    return RuntimeCalibrationPolicy(
        metadata=CalibrationPolicyMetadata(
            policy_id=policy_id,
            service=service,
            contract_version=contract_version,
            policy_version="1.0.0",
            benchmark_attestation_id="benchmark-attestation-1",
            model_identifier=model_identifier,
            payload_hash=payload_hash,
            signature="signature-test",
        ),
        private_payload={
            "calibration_parameters": {
                "decision_offset": 1.0,
            }
        },
    )


def make_registry() -> TrustedCalibrationRegistry:
    return TrustedCalibrationRegistry(
        [
            TrustedCalibrationPolicyRef(
                policy_id="core-policy-v1",
                service="core",
                contract_version="2.6",
                model_identifier="credona.age.age-gender-onnx.v1",
                payload_hash="sha256:test",
                public_key_id="core-key-1",
            )
        ]
    )


def test_trusted_calibration_registry_accepts_known_policy() -> None:
    make_registry().assert_trusted(make_policy())


def test_trusted_calibration_registry_rejects_unknown_policy() -> None:
    with pytest.raises(CalibrationActivationError, match="CALIBRATION_POLICY_NOT_TRUSTED"):
        make_registry().assert_trusted(make_policy(policy_id="unknown-policy"))


def test_trusted_calibration_registry_rejects_service_mismatch() -> None:
    with pytest.raises(CalibrationActivationError, match="CALIBRATION_TRUSTED_SERVICE_MISMATCH"):
        make_registry().assert_trusted(make_policy(service="antispoof"))


def test_trusted_calibration_registry_rejects_contract_mismatch() -> None:
    with pytest.raises(CalibrationActivationError, match="CALIBRATION_TRUSTED_CONTRACT_MISMATCH"):
        make_registry().assert_trusted(make_policy(contract_version="2.5"))


def test_trusted_calibration_registry_rejects_model_mismatch() -> None:
    with pytest.raises(CalibrationActivationError, match="CALIBRATION_TRUSTED_MODEL_MISMATCH"):
        make_registry().assert_trusted(make_policy(model_identifier="another-model"))


def test_trusted_calibration_registry_rejects_hash_mismatch() -> None:
    with pytest.raises(CalibrationActivationError, match="CALIBRATION_TRUSTED_HASH_MISMATCH"):
        make_registry().assert_trusted(make_policy(payload_hash="sha256:other"))
