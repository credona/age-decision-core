import json
from pathlib import Path
from typing import Any

from app.application.calibration.ports import (
    CalibrationActivationStorePort,
    CalibrationProvenanceStorePort,
    CalibrationRollbackStorePort,
)
from app.domain.calibration import (
    CalibrationActivationError,
    CalibrationActivationRecord,
    CalibrationPolicyMetadata,
    CalibrationProvenanceEvent,
    CalibrationRollbackRecord,
    RuntimeCalibrationPolicy,
)


class FileCalibrationLifecycleStore(
    CalibrationActivationStorePort,
    CalibrationRollbackStorePort,
    CalibrationProvenanceStorePort,
):
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.active_file = self.directory / "active_policy.json"
        self.previous_file = self.directory / "previous_policy.json"
        self.provenance_file = self.directory / "provenance.jsonl"
        self.rollback_file = self.directory / "rollback_records.jsonl"

    def get_active_policy(self) -> RuntimeCalibrationPolicy | None:
        return self._read_policy(self.active_file)

    def set_active_policy(
        self,
        policy: RuntimeCalibrationPolicy,
        activation_record: CalibrationActivationRecord,
    ) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)

        current = self.get_active_policy()
        if current is not None:
            self._write_policy(self.previous_file, current)

        self._write_policy(self.active_file, policy)

    def get_previous_policy(self) -> RuntimeCalibrationPolicy | None:
        return self._read_policy(self.previous_file)

    def set_previous_policy(self, policy: RuntimeCalibrationPolicy | None) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)

        if policy is None:
            self.previous_file.unlink(missing_ok=True)
            return

        self._write_policy(self.previous_file, policy)

    def save_rollback_record(self, record: CalibrationRollbackRecord) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        self._append_jsonl(self.rollback_file, record.to_public_dict())

    def append(self, event: CalibrationProvenanceEvent) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        self._append_jsonl(self.provenance_file, event.to_public_dict())

    def list_events(self) -> list[dict[str, str]]:
        if not self.provenance_file.exists():
            return []

        events = []
        for line in self.provenance_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                parsed = json.loads(line)
                if isinstance(parsed, dict):
                    events.append({str(key): str(value) for key, value in parsed.items()})

        return events

    def _read_policy(self, path: Path) -> RuntimeCalibrationPolicy | None:
        if not path.exists():
            return None

        try:
            document = json.loads(path.read_text(encoding="utf-8"))
            metadata = document["metadata"]
            return RuntimeCalibrationPolicy(
                metadata=CalibrationPolicyMetadata(
                    policy_id=metadata["policy_id"],
                    service=metadata["service"],
                    contract_version=metadata["contract_version"],
                    policy_version=metadata["policy_version"],
                    benchmark_attestation_id=metadata["benchmark_attestation_id"],
                    model_identifier=metadata["model_identifier"],
                    payload_hash=metadata["payload_hash"],
                    signature=metadata["signature"],
                ),
                private_payload=document["private_payload"],
            )
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise CalibrationActivationError("CALIBRATION_STORED_POLICY_INVALID") from exc

    def _write_policy(self, path: Path, policy: RuntimeCalibrationPolicy) -> None:
        document = {
            "metadata": {
                "policy_id": policy.metadata.policy_id,
                "service": policy.metadata.service,
                "contract_version": policy.metadata.contract_version,
                "policy_version": policy.metadata.policy_version,
                "benchmark_attestation_id": policy.metadata.benchmark_attestation_id,
                "model_identifier": policy.metadata.model_identifier,
                "payload_hash": policy.metadata.payload_hash,
                "signature": policy.metadata.signature,
            },
            "private_payload": dict(policy.private_payload),
        }

        path.write_text(
            json.dumps(document, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )

    def _append_jsonl(self, path: Path, payload: dict[str, Any]) -> None:
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
            file.write("\n")
