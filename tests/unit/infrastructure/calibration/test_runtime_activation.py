import base64
import hashlib
import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.domain.calibration import CalibrationActivationError
from app.infrastructure.calibration.runtime_activation import (
    get_core_calibration_provenance,
    load_core_runtime_calibration,
    rollback_core_runtime_calibration,
)
from app.infrastructure.config.settings import settings
from app.project import project_metadata


def canonical_payload(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def write_signed_policy(path: Path, policy_id: str = "core-runtime-policy-test") -> str:
    payload = {
        "calibration_parameters": {
            "decision_offset": 0.0,
            "signal_quality_floor": 0.0,
        }
    }

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    payload_bytes = canonical_payload(payload)

    document = {
        "metadata": {
            "policy_id": policy_id,
            "service": "core",
            "contract_version": project_metadata.contract_version,
            "policy_version": "1.0.0",
            "benchmark_attestation_id": f"benchmark-attestation-{policy_id}",
            "model_identifier": settings.age_model_id,
            "payload_hash": f"sha256:{hashlib.sha256(payload_bytes).hexdigest()}",
            "signature": base64.b64encode(private_key.sign(payload_bytes)).decode("ascii"),
        },
        "private_payload": payload,
    }

    path.write_text(json.dumps(document), encoding="utf-8")

    return base64.b64encode(public_key.public_bytes_raw()).decode("ascii")


def test_runtime_activation_returns_none_when_calibration_is_not_required(monkeypatch) -> None:
    monkeypatch.setattr(settings, "core_calibration_required", False)
    monkeypatch.setattr(settings, "core_calibration_policy_path", None)
    monkeypatch.setattr(settings, "core_calibration_public_key_b64", None)

    assert load_core_runtime_calibration() is None


def test_runtime_activation_rejects_missing_policy_when_required(monkeypatch) -> None:
    monkeypatch.setattr(settings, "core_calibration_required", True)
    monkeypatch.setattr(settings, "core_calibration_policy_path", None)
    monkeypatch.setattr(settings, "core_calibration_public_key_b64", None)

    with pytest.raises(CalibrationActivationError, match="CALIBRATION_POLICY_PATH_MISSING"):
        load_core_runtime_calibration()


def test_runtime_activation_loads_valid_signed_policy(tmp_path: Path, monkeypatch) -> None:
    policy_path = tmp_path / "core-policy.private.json"
    state_dir = tmp_path / "state"
    public_key_b64 = write_signed_policy(policy_path)

    monkeypatch.setattr(settings, "core_calibration_required", True)
    monkeypatch.setattr(settings, "core_calibration_policy_path", str(policy_path))
    monkeypatch.setattr(settings, "core_calibration_public_key_b64", public_key_b64)
    monkeypatch.setattr(settings, "core_calibration_state_dir", str(state_dir))

    policy = load_core_runtime_calibration()

    assert policy is not None
    assert policy.metadata.service == "core"
    assert policy.metadata.model_identifier == settings.age_model_id
    assert (state_dir / "active_policy.json").exists()

    events = get_core_calibration_provenance()
    assert len(events) == 1
    assert events[0]["event"] == "calibration_activated"
    assert events[0]["policy_id"] == "core-runtime-policy-test"


def test_runtime_activation_rollback_restores_previous_policy(
    tmp_path: Path,
    monkeypatch,
) -> None:
    state_dir = tmp_path / "state"

    policy_path_v1 = tmp_path / "core-policy-v1.private.json"
    public_key_v1 = write_signed_policy(policy_path_v1, policy_id="core-policy-v1")

    monkeypatch.setattr(settings, "core_calibration_required", True)
    monkeypatch.setattr(settings, "core_calibration_policy_path", str(policy_path_v1))
    monkeypatch.setattr(settings, "core_calibration_public_key_b64", public_key_v1)
    monkeypatch.setattr(settings, "core_calibration_state_dir", str(state_dir))

    load_core_runtime_calibration()

    policy_path_v2 = tmp_path / "core-policy-v2.private.json"
    public_key_v2 = write_signed_policy(policy_path_v2, policy_id="core-policy-v2")

    monkeypatch.setattr(settings, "core_calibration_policy_path", str(policy_path_v2))
    monkeypatch.setattr(settings, "core_calibration_public_key_b64", public_key_v2)

    load_core_runtime_calibration()

    restored = rollback_core_runtime_calibration()

    assert restored.metadata.policy_id == "core-policy-v1"

    events = get_core_calibration_provenance()
    assert [event["event"] for event in events] == [
        "calibration_activated",
        "calibration_activated",
        "calibration_rolled_back",
    ]
    assert events[-1]["from_policy_id"] == "core-policy-v2"
    assert events[-1]["to_policy_id"] == "core-policy-v1"


def test_runtime_activation_loads_policy_with_manifest_and_registry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    policy_path = tmp_path / "core-policy.private.json"
    state_dir = tmp_path / "state"
    manifest_path = tmp_path / "manifest.json"
    registry_path = tmp_path / "registry.json"

    public_key_b64 = write_signed_policy(policy_path, policy_id="core-policy-v1")

    document = json.loads(policy_path.read_text(encoding="utf-8"))
    metadata = document["metadata"]

    manifest_path.write_text(
        json.dumps(
            {
                "manifest_id": "core-manifest-v1",
                "service": "core",
                "contract_version": project_metadata.contract_version,
                "policy_ids": ["core-policy-v1"],
            }
        ),
        encoding="utf-8",
    )

    registry_path.write_text(
        json.dumps(
            {
                "policies": [
                    {
                        "policy_id": metadata["policy_id"],
                        "service": metadata["service"],
                        "contract_version": metadata["contract_version"],
                        "model_identifier": metadata["model_identifier"],
                        "payload_hash": metadata["payload_hash"],
                        "public_key_id": "core-key-1",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(settings, "core_calibration_required", True)
    monkeypatch.setattr(settings, "core_calibration_policy_path", str(policy_path))
    monkeypatch.setattr(settings, "core_calibration_public_key_b64", public_key_b64)
    monkeypatch.setattr(settings, "core_calibration_state_dir", str(state_dir))
    monkeypatch.setattr(settings, "core_calibration_manifest_path", str(manifest_path))
    monkeypatch.setattr(settings, "core_calibration_registry_path", str(registry_path))

    policy = load_core_runtime_calibration()

    assert policy is not None
    assert policy.metadata.policy_id == "core-policy-v1"
    assert (state_dir / "active_policy.json").exists()
