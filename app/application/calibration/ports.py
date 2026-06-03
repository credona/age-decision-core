from typing import Protocol

from app.domain.calibration import (
    CalibrationActivationRecord,
    CalibrationProvenanceEvent,
    CalibrationRollbackRecord,
    RuntimeCalibrationPolicy,
)


class CalibrationPolicyReaderPort(Protocol):
    def read_policy_bytes(self) -> bytes: ...


class CalibrationIntegrityVerifierPort(Protocol):
    def verify(self, *, payload: bytes, expected_hash: str) -> bool: ...


class CalibrationSignatureVerifierPort(Protocol):
    def verify(self, *, payload: bytes, signature: str) -> bool: ...


class CalibrationActivationStorePort(Protocol):
    def get_active_policy(self) -> RuntimeCalibrationPolicy | None: ...

    def set_active_policy(
        self,
        policy: RuntimeCalibrationPolicy,
        activation_record: CalibrationActivationRecord,
    ) -> None: ...


class CalibrationRollbackStorePort(Protocol):
    def get_previous_policy(self) -> RuntimeCalibrationPolicy | None: ...

    def set_previous_policy(self, policy: RuntimeCalibrationPolicy | None) -> None: ...

    def save_rollback_record(self, record: CalibrationRollbackRecord) -> None: ...


class CalibrationProvenanceStorePort(Protocol):
    def append(self, event: CalibrationProvenanceEvent) -> None: ...

    def list_events(self) -> list[dict[str, str]]: ...
