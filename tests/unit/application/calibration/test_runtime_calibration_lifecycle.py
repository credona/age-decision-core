import pytest

from app.application.calibration.activate_runtime_calibration import (
    ActivateRuntimeCalibrationUseCase,
)
from app.application.calibration.rollback_runtime_calibration import (
    RollbackRuntimeCalibrationUseCase,
)
from app.domain.calibration import (
    CalibrationActivationError,
    CalibrationPolicyMetadata,
    RuntimeCalibrationPolicy,
)
from app.infrastructure.calibration.memory_lifecycle_store import (
    MemoryCalibrationLifecycleStore,
)


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
                "decision_offset": 0.0,
            }
        },
    )


def test_activate_runtime_calibration_sets_active_policy_and_provenance() -> None:
    store = MemoryCalibrationLifecycleStore()
    policy = make_policy("core-policy-v1", "1.0.0")

    record = ActivateRuntimeCalibrationUseCase(store, store).execute(policy=policy)

    assert store.get_active_policy() == policy
    assert record.policy_id == "core-policy-v1"

    events = store.list_events()
    assert len(events) == 1
    assert events[0]["event"] == "calibration_activated"
    assert events[0]["policy_id"] == "core-policy-v1"


def test_activate_runtime_calibration_keeps_previous_policy() -> None:
    store = MemoryCalibrationLifecycleStore()
    use_case = ActivateRuntimeCalibrationUseCase(store, store)

    policy_v1 = make_policy("core-policy-v1", "1.0.0")
    policy_v2 = make_policy("core-policy-v2", "2.0.0")

    use_case.execute(policy=policy_v1)
    use_case.execute(policy=policy_v2)

    assert store.get_active_policy() == policy_v2
    assert store.get_previous_policy() == policy_v1


def test_rollback_runtime_calibration_restores_previous_policy() -> None:
    store = MemoryCalibrationLifecycleStore()
    activate = ActivateRuntimeCalibrationUseCase(store, store)
    rollback = RollbackRuntimeCalibrationUseCase(store, store, store)

    policy_v1 = make_policy("core-policy-v1", "1.0.0")
    policy_v2 = make_policy("core-policy-v2", "2.0.0")

    activate.execute(policy=policy_v1)
    activate.execute(policy=policy_v2)

    restored = rollback.execute()

    assert restored == policy_v1
    assert store.get_active_policy() == policy_v1

    events = store.list_events()
    assert [event["event"] for event in events] == [
        "calibration_activated",
        "calibration_activated",
        "calibration_rolled_back",
    ]
    assert events[-1]["from_policy_id"] == "core-policy-v2"
    assert events[-1]["to_policy_id"] == "core-policy-v1"


def test_rollback_runtime_calibration_rejects_missing_active_policy() -> None:
    store = MemoryCalibrationLifecycleStore()

    with pytest.raises(CalibrationActivationError, match="CALIBRATION_ACTIVE_POLICY_MISSING"):
        RollbackRuntimeCalibrationUseCase(store, store, store).execute()


def test_rollback_runtime_calibration_rejects_missing_previous_policy() -> None:
    store = MemoryCalibrationLifecycleStore()
    policy = make_policy("core-policy-v1", "1.0.0")

    ActivateRuntimeCalibrationUseCase(store, store).execute(policy=policy)

    with pytest.raises(CalibrationActivationError, match="CALIBRATION_PREVIOUS_POLICY_MISSING"):
        RollbackRuntimeCalibrationUseCase(store, store, store).execute()
