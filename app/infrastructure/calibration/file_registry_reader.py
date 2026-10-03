import json
from pathlib import Path
from typing import Any

from app.domain.calibration import (
    CalibrationActivationError,
    TrustedCalibrationPolicyRef,
    TrustedCalibrationRegistry,
)


class FileTrustedCalibrationRegistryReader:
    def __init__(self, path: str | None):
        self.path = path

    def read(self) -> TrustedCalibrationRegistry | None:
        if not self.path:
            return None

        registry_path = Path(self.path)

        if not registry_path.exists() or not registry_path.is_file():
            raise CalibrationActivationError("CALIBRATION_REGISTRY_FILE_MISSING")

        try:
            document = json.loads(registry_path.read_text(encoding="utf-8"))
            return self._build_registry(document)
        except json.JSONDecodeError as exc:
            raise CalibrationActivationError("CALIBRATION_REGISTRY_INVALID_JSON") from exc

    def _build_registry(self, document: dict[str, Any]) -> TrustedCalibrationRegistry:
        try:
            policies = document["policies"]

            if not isinstance(policies, list):
                raise CalibrationActivationError("CALIBRATION_REGISTRY_INVALID_POLICIES")

            return TrustedCalibrationRegistry(
                [self._build_policy_ref(policy) for policy in policies]
            )
        except KeyError as exc:
            raise CalibrationActivationError("CALIBRATION_REGISTRY_INVALID") from exc

    def _build_policy_ref(self, document: dict[str, Any]) -> TrustedCalibrationPolicyRef:
        try:
            return TrustedCalibrationPolicyRef(
                policy_id=document["policy_id"],
                service=document["service"],
                contract_version=document["contract_version"],
                model_identifier=document["model_identifier"],
                payload_hash=document["payload_hash"],
                public_key_id=document["public_key_id"],
            )
        except KeyError as exc:
            raise CalibrationActivationError("CALIBRATION_REGISTRY_POLICY_INVALID") from exc
