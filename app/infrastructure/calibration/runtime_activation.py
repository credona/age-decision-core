from app.application.calibration.load_runtime_calibration import LoadRuntimeCalibrationUseCase
from app.domain.calibration import RuntimeCalibrationPolicy
from app.infrastructure.calibration.ed25519_signature_verifier import (
    Ed25519CalibrationSignatureVerifier,
)
from app.infrastructure.calibration.file_policy_reader import FileCalibrationPolicyReader
from app.infrastructure.calibration.sha256_integrity_verifier import (
    Sha256CalibrationIntegrityVerifier,
)
from app.infrastructure.config.settings import settings
from app.project import project_metadata


def load_core_runtime_calibration() -> RuntimeCalibrationPolicy | None:
    if not settings.core_calibration_required and not settings.core_calibration_policy_path:
        return None

    use_case = LoadRuntimeCalibrationUseCase(
        reader=FileCalibrationPolicyReader(settings.core_calibration_policy_path),
        integrity_verifier=Sha256CalibrationIntegrityVerifier(),
        signature_verifier=Ed25519CalibrationSignatureVerifier(
            settings.core_calibration_public_key_b64
        ),
    )

    return use_case.execute(
        expected_service="core",
        expected_contract_version=project_metadata.contract_version,
        expected_model_identifier=settings.age_model_id,
    )
