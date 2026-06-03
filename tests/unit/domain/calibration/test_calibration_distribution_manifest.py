import pytest

from app.domain.calibration import (
    CalibrationActivationError,
    CalibrationDistributionManifest,
    CalibrationPolicyMetadata,
    RuntimeCalibrationPolicy,
)


def make_policy(
    *,
    policy_id: str = "core-policy-v1",
    service: str = "core",
    contract_version: str = "2.6",
) -> RuntimeCalibrationPolicy:
    return RuntimeCalibrationPolicy(
        metadata=CalibrationPolicyMetadata(
            policy_id=policy_id,
            service=service,
            contract_version=contract_version,
            policy_version="1.0.0",
            benchmark_attestation_id="benchmark-attestation-1",
            model_identifier="credona.age.age-gender-onnx.v1",
            payload_hash="sha256:test",
            signature="signature-test",
        ),
        private_payload={
            "calibration_parameters": {
                "decision_offset": 1.0,
            }
        },
    )


def make_manifest() -> CalibrationDistributionManifest:
    return CalibrationDistributionManifest(
        manifest_id="core-manifest-v1",
        service="core",
        contract_version="2.6",
        policy_ids=("core-policy-v1",),
    )


def test_distribution_manifest_accepts_allowed_policy() -> None:
    make_manifest().assert_allows(make_policy())


def test_distribution_manifest_rejects_service_mismatch() -> None:
    with pytest.raises(CalibrationActivationError, match="CALIBRATION_MANIFEST_SERVICE_MISMATCH"):
        make_manifest().assert_allows(make_policy(service="antispoof"))


def test_distribution_manifest_rejects_contract_mismatch() -> None:
    with pytest.raises(CalibrationActivationError, match="CALIBRATION_MANIFEST_CONTRACT_MISMATCH"):
        make_manifest().assert_allows(make_policy(contract_version="2.5"))


def test_distribution_manifest_rejects_unknown_policy() -> None:
    with pytest.raises(CalibrationActivationError, match="CALIBRATION_POLICY_NOT_IN_MANIFEST"):
        make_manifest().assert_allows(make_policy(policy_id="unknown-policy"))
