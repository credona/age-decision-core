from dataclasses import dataclass

from app.domain.calibration.errors import CalibrationActivationError
from app.domain.calibration.policy import RuntimeCalibrationPolicy


@dataclass(frozen=True)
class TrustedCalibrationPolicyRef:
    policy_id: str
    service: str
    contract_version: str
    model_identifier: str
    payload_hash: str
    public_key_id: str


class TrustedCalibrationRegistry:
    def __init__(self, policies: list[TrustedCalibrationPolicyRef]):
        self._policies = {policy.policy_id: policy for policy in policies}

    def assert_trusted(self, policy: RuntimeCalibrationPolicy) -> None:
        trusted = self._policies.get(policy.metadata.policy_id)

        if trusted is None:
            raise CalibrationActivationError("CALIBRATION_POLICY_NOT_TRUSTED")

        if trusted.service != policy.metadata.service:
            raise CalibrationActivationError("CALIBRATION_TRUSTED_SERVICE_MISMATCH")

        if trusted.contract_version != policy.metadata.contract_version:
            raise CalibrationActivationError("CALIBRATION_TRUSTED_CONTRACT_MISMATCH")

        if trusted.model_identifier != policy.metadata.model_identifier:
            raise CalibrationActivationError("CALIBRATION_TRUSTED_MODEL_MISMATCH")

        if trusted.payload_hash != policy.metadata.payload_hash:
            raise CalibrationActivationError("CALIBRATION_TRUSTED_HASH_MISMATCH")
