from dataclasses import dataclass

from app.domain.calibration.policy import RuntimeCalibrationPolicy


@dataclass(frozen=True)
class CalibratedCoreSignal:
    internal_estimate: float
    signal_quality_score: float


class CoreCalibrationApplier:
    def __init__(self, policy: RuntimeCalibrationPolicy | None = None):
        self.policy = policy

    def apply(
        self,
        *,
        internal_estimate: float,
        signal_quality_score: float,
    ) -> CalibratedCoreSignal:
        if self.policy is None:
            return CalibratedCoreSignal(
                internal_estimate=self._clamp_age(internal_estimate),
                signal_quality_score=self._clamp_score(signal_quality_score),
            )

        parameters = self.policy.private_payload.get("calibration_parameters", {})

        decision_offset = self._as_float(parameters.get("decision_offset", 0.0))
        signal_quality_offset = self._as_float(parameters.get("signal_quality_offset", 0.0))
        signal_quality_floor = self._as_float(parameters.get("signal_quality_floor", 0.0))
        signal_quality_ceiling = self._as_float(parameters.get("signal_quality_ceiling", 1.0))

        calibrated_age = self._clamp_age(internal_estimate + decision_offset)
        calibrated_signal_quality = self._clamp_score(signal_quality_score + signal_quality_offset)
        calibrated_signal_quality = max(calibrated_signal_quality, signal_quality_floor)
        calibrated_signal_quality = min(calibrated_signal_quality, signal_quality_ceiling)

        return CalibratedCoreSignal(
            internal_estimate=calibrated_age,
            signal_quality_score=self._clamp_score(calibrated_signal_quality),
        )

    def _as_float(self, value: object) -> float:
        if isinstance(value, bool):
            return 0.0

        if isinstance(value, int | float):
            return float(value)

        return 0.0

    def _clamp_age(self, value: float) -> float:
        return round(min(max(float(value), 0.0), 120.0), 6)

    def _clamp_score(self, value: float) -> float:
        return round(min(max(float(value), 0.0), 1.0), 6)
