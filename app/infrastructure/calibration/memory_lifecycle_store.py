from app.application.calibration.ports import (
    CalibrationActivationStorePort,
    CalibrationProvenanceStorePort,
    CalibrationRollbackStorePort,
)
from app.domain.calibration import (
    CalibrationActivationRecord,
    CalibrationProvenanceChain,
    CalibrationProvenanceEvent,
    CalibrationRollbackRecord,
    RuntimeCalibrationPolicy,
)


class MemoryCalibrationLifecycleStore(
    CalibrationActivationStorePort,
    CalibrationRollbackStorePort,
    CalibrationProvenanceStorePort,
):
    def __init__(self):
        self._active_policy: RuntimeCalibrationPolicy | None = None
        self._previous_policy: RuntimeCalibrationPolicy | None = None
        self._activation_records: list[CalibrationActivationRecord] = []
        self._rollback_records: list[CalibrationRollbackRecord] = []
        self._provenance = CalibrationProvenanceChain()

    def get_active_policy(self) -> RuntimeCalibrationPolicy | None:
        return self._active_policy

    def set_active_policy(
        self,
        policy: RuntimeCalibrationPolicy,
        activation_record: CalibrationActivationRecord,
    ) -> None:
        if self._active_policy is not None:
            self._previous_policy = self._active_policy

        self._active_policy = policy
        self._activation_records.append(activation_record)

    def get_previous_policy(self) -> RuntimeCalibrationPolicy | None:
        return self._previous_policy

    def set_previous_policy(self, policy: RuntimeCalibrationPolicy | None) -> None:
        self._previous_policy = policy

    def save_rollback_record(self, record: CalibrationRollbackRecord) -> None:
        self._rollback_records.append(record)

    def append(self, event: CalibrationProvenanceEvent) -> None:
        self._provenance.append(event)

    def list_events(self) -> list[dict[str, str]]:
        return self._provenance.to_public_list()
