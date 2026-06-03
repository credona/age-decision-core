from dataclasses import dataclass

from app.domain.calibration.errors import CalibrationActivationError
from app.domain.calibration.policy import RuntimeCalibrationPolicy


@dataclass(frozen=True)
class CalibrationDistributionManifest:
    manifest_id: str
    service: str
    contract_version: str
    policy_ids: tuple[str, ...]

    def assert_allows(self, policy: RuntimeCalibrationPolicy) -> None:
        if self.service != policy.metadata.service:
            raise CalibrationActivationError("CALIBRATION_MANIFEST_SERVICE_MISMATCH")

        if self.contract_version != policy.metadata.contract_version:
            raise CalibrationActivationError("CALIBRATION_MANIFEST_CONTRACT_MISMATCH")

        if policy.metadata.policy_id not in self.policy_ids:
            raise CalibrationActivationError("CALIBRATION_POLICY_NOT_IN_MANIFEST")
