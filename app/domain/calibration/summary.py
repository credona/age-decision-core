from dataclasses import dataclass

from app.domain.calibration.policy import RuntimeCalibrationPolicy


@dataclass(frozen=True)
class PublicCalibrationSummary:
    policy_id: str
    policy_version: str
    benchmark_attestation_id: str
    model_identifier: str
    service: str
    contract_version: str
    active: bool

    @classmethod
    def from_policy(
        cls,
        policy: RuntimeCalibrationPolicy,
        *,
        active: bool,
    ) -> "PublicCalibrationSummary":
        return cls(
            policy_id=policy.metadata.policy_id,
            policy_version=policy.metadata.policy_version,
            benchmark_attestation_id=policy.metadata.benchmark_attestation_id,
            model_identifier=policy.metadata.model_identifier,
            service=policy.metadata.service,
            contract_version=policy.metadata.contract_version,
            active=active,
        )

    def to_public_dict(self) -> dict[str, str | bool]:
        return {
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "benchmark_attestation_id": self.benchmark_attestation_id,
            "model_identifier": self.model_identifier,
            "service": self.service,
            "contract_version": self.contract_version,
            "active": self.active,
        }
