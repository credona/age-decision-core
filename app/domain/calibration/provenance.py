from app.domain.calibration.activation import (
    CalibrationActivationRecord,
    CalibrationRollbackRecord,
)

CalibrationProvenanceEvent = CalibrationActivationRecord | CalibrationRollbackRecord


class CalibrationProvenanceChain:
    def __init__(self, events: list[CalibrationProvenanceEvent] | None = None):
        self._events = tuple(events or [])

    def append(self, event: CalibrationProvenanceEvent) -> None:
        self._events = (*self._events, event)

    def to_public_list(self) -> list[dict[str, str]]:
        return [event.to_public_dict() for event in self._events]
