from app.domain.calibration.activation import (
    CalibrationActivationRecord,
    CalibrationRollbackRecord,
)
from app.domain.calibration.provenance import CalibrationProvenanceChain


def test_activation_record_is_public_safe() -> None:
    record = CalibrationActivationRecord.create(
        policy_id="core-policy-v1",
        policy_version="1.0.0",
        benchmark_attestation_id="benchmark-attestation-1",
        model_identifier="credona.age.age-gender-onnx.v1",
        activated_by="runtime",
    )

    exported = record.to_public_dict()

    assert exported == {
        "event": "calibration_activated",
        "policy_id": "core-policy-v1",
        "policy_version": "1.0.0",
        "benchmark_attestation_id": "benchmark-attestation-1",
        "model_identifier": "credona.age.age-gender-onnx.v1",
        "activated_by": "runtime",
        "created_at": record.created_at,
    }


def test_rollback_record_is_public_safe() -> None:
    record = CalibrationRollbackRecord.create(
        from_policy_id="core-policy-v2",
        to_policy_id="core-policy-v1",
        reason_code="CALIBRATION_RUNTIME_ROLLBACK",
        rolled_back_by="runtime",
    )

    exported = record.to_public_dict()

    assert exported == {
        "event": "calibration_rolled_back",
        "from_policy_id": "core-policy-v2",
        "to_policy_id": "core-policy-v1",
        "reason_code": "CALIBRATION_RUNTIME_ROLLBACK",
        "rolled_back_by": "runtime",
        "created_at": record.created_at,
    }


def test_provenance_chain_is_append_only() -> None:
    chain = CalibrationProvenanceChain()

    activation = CalibrationActivationRecord.create(
        policy_id="core-policy-v1",
        policy_version="1.0.0",
        benchmark_attestation_id="benchmark-attestation-1",
        model_identifier="credona.age.age-gender-onnx.v1",
        activated_by="runtime",
    )

    rollback = CalibrationRollbackRecord.create(
        from_policy_id="core-policy-v2",
        to_policy_id="core-policy-v1",
        reason_code="CALIBRATION_RUNTIME_ROLLBACK",
        rolled_back_by="runtime",
    )

    chain.append(activation)
    chain.append(rollback)

    events = chain.to_public_list()

    assert len(events) == 2
    assert events[0]["event"] == "calibration_activated"
    assert events[1]["event"] == "calibration_rolled_back"

    events.append({"event": "tampered"})

    assert len(chain.to_public_list()) == 2
