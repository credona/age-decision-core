import base64
import hashlib
import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.domain.calibration import CalibrationActivationError
from app.infrastructure.calibration.runtime_activation import load_core_runtime_calibration
from app.infrastructure.config.settings import settings
from app.project import project_metadata


def canonical_payload(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def write_signed_policy(path: Path) -> str:
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
            "policy_id": "core-runtime-policy-test",
            "service": "core",
            "contract_version": project_metadata.contract_version,
            "policy_version": "1.0.0",
            "benchmark_attestation_id": "benchmark-attestation-test",
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
    public_key_b64 = write_signed_policy(policy_path)

    monkeypatch.setattr(settings, "core_calibration_required", True)
    monkeypatch.setattr(settings, "core_calibration_policy_path", str(policy_path))
    monkeypatch.setattr(settings, "core_calibration_public_key_b64", public_key_b64)

    policy = load_core_runtime_calibration()

    assert policy is not None
    assert policy.metadata.service == "core"
    assert policy.metadata.model_identifier == settings.age_model_id
