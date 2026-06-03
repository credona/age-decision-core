import json
from pathlib import Path
from typing import Any

from app.domain.calibration import (
    CalibrationActivationError,
    CalibrationDistributionManifest,
)


class FileCalibrationManifestReader:
    def __init__(self, path: str | None):
        self.path = path

    def read(self) -> CalibrationDistributionManifest | None:
        if not self.path:
            return None

        manifest_path = Path(self.path)

        if not manifest_path.exists() or not manifest_path.is_file():
            raise CalibrationActivationError("CALIBRATION_MANIFEST_FILE_MISSING")

        try:
            document = json.loads(manifest_path.read_text(encoding="utf-8"))
            return self._build_manifest(document)
        except json.JSONDecodeError as exc:
            raise CalibrationActivationError("CALIBRATION_MANIFEST_INVALID_JSON") from exc

    def _build_manifest(self, document: dict[str, Any]) -> CalibrationDistributionManifest:
        try:
            policy_ids = document["policy_ids"]

            if not isinstance(policy_ids, list) or not all(
                isinstance(policy_id, str) for policy_id in policy_ids
            ):
                raise CalibrationActivationError("CALIBRATION_MANIFEST_INVALID_POLICY_IDS")

            return CalibrationDistributionManifest(
                manifest_id=document["manifest_id"],
                service=document["service"],
                contract_version=document["contract_version"],
                policy_ids=tuple(policy_ids),
            )
        except KeyError as exc:
            raise CalibrationActivationError("CALIBRATION_MANIFEST_INVALID") from exc
