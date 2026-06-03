from app.application.calibration.ports import (
    CalibrationActivationStorePort,
    CalibrationProvenanceStorePort,
    CalibrationRollbackStorePort,
)
from app.domain.calibration import (
    CalibrationActivationError,
    CalibrationRollbackRecord,
    RuntimeCalibrationPolicy,
)


class RollbackRuntimeCalibrationUseCase:
    def __init__(
        self,
        activation_store: CalibrationActivationStorePort,
        rollback_store: CalibrationRollbackStorePort,
        provenance_store: CalibrationProvenanceStorePort,
    ):
        self.activation_store = activation_store
        self.rollback_store = rollback_store
        self.provenance_store = provenance_store

    def execute(
        self,
        *,
        reason_code: str = "CALIBRATION_RUNTIME_ROLLBACK",
        rolled_back_by: str = "runtime",
    ) -> RuntimeCalibrationPolicy:
        active_policy = self.activation_store.get_active_policy()
        previous_policy = self.rollback_store.get_previous_policy()

        if active_policy is None:
            raise CalibrationActivationError("CALIBRATION_ACTIVE_POLICY_MISSING")

        if previous_policy is None:
            raise CalibrationActivationError("CALIBRATION_PREVIOUS_POLICY_MISSING")

        record = CalibrationRollbackRecord.create(
            from_policy_id=active_policy.metadata.policy_id,
            to_policy_id=previous_policy.metadata.policy_id,
            reason_code=reason_code,
            rolled_back_by=rolled_back_by,
        )

        self.activation_store.set_active_policy(
            previous_policy,
            CalibrationActivationRecordLike.from_rollback(record, previous_policy),
        )
        self.rollback_store.save_rollback_record(record)
        self.provenance_store.append(record)

        return previous_policy


class CalibrationActivationRecordLike:
    @staticmethod
    def from_rollback(
        record: CalibrationRollbackRecord,
        policy: RuntimeCalibrationPolicy,
    ):
        from app.domain.calibration import CalibrationActivationRecord

        return CalibrationActivationRecord(
            policy_id=policy.metadata.policy_id,
            policy_version=policy.metadata.policy_version,
            benchmark_attestation_id=policy.metadata.benchmark_attestation_id,
            model_identifier=policy.metadata.model_identifier,
            activated_by=record.rolled_back_by,
            created_at=record.created_at,
            event="calibration_activated",
        )
