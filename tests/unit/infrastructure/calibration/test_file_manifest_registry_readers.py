import json
from pathlib import Path

import pytest

from app.domain.calibration import CalibrationActivationError
from app.infrastructure.calibration.file_manifest_reader import FileCalibrationManifestReader
from app.infrastructure.calibration.file_registry_reader import FileTrustedCalibrationRegistryReader


def test_file_manifest_reader_returns_none_without_path() -> None:
    assert FileCalibrationManifestReader(None).read() is None


def test_file_manifest_reader_reads_manifest(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(
        json.dumps(
            {
                "manifest_id": "core-manifest-v1",
                "service": "core",
                "contract_version": "2.6",
                "policy_ids": ["core-policy-v1"],
            }
        ),
        encoding="utf-8",
    )

    manifest = FileCalibrationManifestReader(str(path)).read()

    assert manifest is not None
    assert manifest.manifest_id == "core-manifest-v1"
    assert manifest.policy_ids == ("core-policy-v1",)


def test_file_manifest_reader_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(CalibrationActivationError, match="CALIBRATION_MANIFEST_FILE_MISSING"):
        FileCalibrationManifestReader(str(tmp_path / "missing.json")).read()


def test_file_manifest_reader_rejects_invalid_policy_ids(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(
        json.dumps(
            {
                "manifest_id": "core-manifest-v1",
                "service": "core",
                "contract_version": "2.6",
                "policy_ids": "core-policy-v1",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        CalibrationActivationError,
        match="CALIBRATION_MANIFEST_INVALID_POLICY_IDS",
    ):
        FileCalibrationManifestReader(str(path)).read()


def test_file_registry_reader_returns_none_without_path() -> None:
    assert FileTrustedCalibrationRegistryReader(None).read() is None


def test_file_registry_reader_reads_registry(tmp_path: Path) -> None:
    path = tmp_path / "registry.json"
    path.write_text(
        json.dumps(
            {
                "policies": [
                    {
                        "policy_id": "core-policy-v1",
                        "service": "core",
                        "contract_version": "2.6",
                        "model_identifier": "credona.age.age-gender-onnx.v1",
                        "payload_hash": "sha256:test",
                        "public_key_id": "core-key-1",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    registry = FileTrustedCalibrationRegistryReader(str(path)).read()

    assert registry is not None


def test_file_registry_reader_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(CalibrationActivationError, match="CALIBRATION_REGISTRY_FILE_MISSING"):
        FileTrustedCalibrationRegistryReader(str(tmp_path / "missing.json")).read()


def test_file_registry_reader_rejects_invalid_policies(tmp_path: Path) -> None:
    path = tmp_path / "registry.json"
    path.write_text(json.dumps({"policies": "invalid"}), encoding="utf-8")

    with pytest.raises(
        CalibrationActivationError,
        match="CALIBRATION_REGISTRY_INVALID_POLICIES",
    ):
        FileTrustedCalibrationRegistryReader(str(path)).read()
