from dataclasses import dataclass
from datetime import UTC, datetime


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


@dataclass(frozen=True)
class CalibrationActivationRecord:
    policy_id: str
    policy_version: str
    benchmark_attestation_id: str
    model_identifier: str
    activated_by: str
    created_at: str
    event: str = "calibration_activated"

    @classmethod
    def create(
        cls,
        *,
        policy_id: str,
        policy_version: str,
        benchmark_attestation_id: str,
        model_identifier: str,
        activated_by: str,
    ) -> "CalibrationActivationRecord":
        return cls(
            policy_id=policy_id,
            policy_version=policy_version,
            benchmark_attestation_id=benchmark_attestation_id,
            model_identifier=model_identifier,
            activated_by=activated_by,
            created_at=_utc_now(),
        )

    def to_public_dict(self) -> dict[str, str]:
        return {
            "event": self.event,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "benchmark_attestation_id": self.benchmark_attestation_id,
            "model_identifier": self.model_identifier,
            "activated_by": self.activated_by,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class CalibrationRollbackRecord:
    from_policy_id: str
    to_policy_id: str
    reason_code: str
    rolled_back_by: str
    created_at: str
    event: str = "calibration_rolled_back"

    @classmethod
    def create(
        cls,
        *,
        from_policy_id: str,
        to_policy_id: str,
        reason_code: str,
        rolled_back_by: str,
    ) -> "CalibrationRollbackRecord":
        return cls(
            from_policy_id=from_policy_id,
            to_policy_id=to_policy_id,
            reason_code=reason_code,
            rolled_back_by=rolled_back_by,
            created_at=_utc_now(),
        )

    def to_public_dict(self) -> dict[str, str]:
        return {
            "event": self.event,
            "from_policy_id": self.from_policy_id,
            "to_policy_id": self.to_policy_id,
            "reason_code": self.reason_code,
            "rolled_back_by": self.rolled_back_by,
            "created_at": self.created_at,
        }
