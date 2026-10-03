import json
from pathlib import Path

import pytest

from app.domain.calibration import (
    CalibrationActivationError,
    CalibrationActivationRecord,
    CalibrationPolicyMetadata,
    CalibrationRollbackRecord,
    RuntimeCalibrationPolicy,
)
from app.infrastructure.calibration.file_lifecycle_store import FileCalibrationLifecycleStore


def make_policy(policy_id: str, version: str) -> RuntimeCalibrationPolicy:
    return RuntimeCalibrationPolicy(
        metadata=CalibrationPolicyMetadata(
            policy_id=policy_id,
            service="core",
            contract_version="2.6",
            policy_version=version,
            benchmark_attestation_id=f"benchmark-{policy_id}",
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


def make_activation(policy: RuntimeCalibrationPolicy) -> CalibrationActivationRecord:
    return CalibrationActivationRecord.create(
        policy_id=policy.metadata.policy_id,
        policy_version=policy.metadata.policy_version,
        benchmark_attestation_id=policy.metadata.benchmark_attestation_id,
        model_identifier=policy.metadata.model_identifier,
        activated_by="runtime",
    )


def test_file_lifecycle_store_persists_active_policy(tmp_path: Path) -> None:
    store = FileCalibrationLifecycleStore(str(tmp_path))
    policy = make_policy("core-policy-v1", "1.0.0")

    store.set_active_policy(policy, make_activation(policy))

    restored = FileCalibrationLifecycleStore(str(tmp_path)).get_active_policy()

    assert restored == policy


def test_file_lifecycle_store_keeps_previous_policy(tmp_path: Path) -> None:
    store = FileCalibrationLifecycleStore(str(tmp_path))

    policy_v1 = make_policy("core-policy-v1", "1.0.0")
    policy_v2 = make_policy("core-policy-v2", "2.0.0")

    store.set_active_policy(policy_v1, make_activation(policy_v1))
    store.set_active_policy(policy_v2, make_activation(policy_v2))

    assert store.get_active_policy() == policy_v2
    assert store.get_previous_policy() == policy_v1


def test_file_lifecycle_store_persists_provenance_events(tmp_path: Path) -> None:
    store = FileCalibrationLifecycleStore(str(tmp_path))
    policy = make_policy("core-policy-v1", "1.0.0")
    activation = make_activation(policy)

    store.append(activation)

    events = FileCalibrationLifecycleStore(str(tmp_path)).list_events()

    assert events == [activation.to_public_dict()]


def test_file_lifecycle_store_persists_rollback_records(tmp_path: Path) -> None:
    store = FileCalibrationLifecycleStore(str(tmp_path))

    record = CalibrationRollbackRecord.create(
        from_policy_id="core-policy-v2",
        to_policy_id="core-policy-v1",
        reason_code="CALIBRATION_RUNTIME_ROLLBACK",
        rolled_back_by="runtime",
    )

    store.save_rollback_record(record)

    rollback_file = tmp_path / "rollback_records.jsonl"
    lines = rollback_file.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 1
    assert json.loads(lines[0]) == record.to_public_dict()


def test_file_lifecycle_store_rejects_invalid_stored_policy(tmp_path: Path) -> None:
    active_file = tmp_path / "active_policy.json"
    active_file.write_text("{invalid-json", encoding="utf-8")

    store = FileCalibrationLifecycleStore(str(tmp_path))

    with pytest.raises(CalibrationActivationError, match="CALIBRATION_STORED_POLICY_INVALID"):
        store.get_active_policy()
