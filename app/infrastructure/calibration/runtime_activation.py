from app.application.calibration.activate_runtime_calibration import (
    ActivateRuntimeCalibrationUseCase,
)
from app.application.calibration.load_runtime_calibration import LoadRuntimeCalibrationUseCase
from app.application.calibration.rollback_runtime_calibration import (
    RollbackRuntimeCalibrationUseCase,
)
from app.domain.calibration import RuntimeCalibrationPolicy
from app.infrastructure.calibration.ed25519_signature_verifier import (
    Ed25519CalibrationSignatureVerifier,
)
from app.infrastructure.calibration.file_lifecycle_store import FileCalibrationLifecycleStore
from app.infrastructure.calibration.file_manifest_reader import FileCalibrationManifestReader
from app.infrastructure.calibration.file_policy_reader import FileCalibrationPolicyReader
from app.infrastructure.calibration.file_registry_reader import (
    FileTrustedCalibrationRegistryReader,
)
from app.infrastructure.calibration.sha256_integrity_verifier import (
    Sha256CalibrationIntegrityVerifier,
)
from app.infrastructure.config.settings import settings
from app.project import project_metadata


def load_core_runtime_calibration() -> RuntimeCalibrationPolicy | None:
    if not settings.core_calibration_required and not settings.core_calibration_policy_path:
        return None

    policy = _load_verified_core_policy()
    store = _core_lifecycle_store()

    ActivateRuntimeCalibrationUseCase(
        activation_store=store,
        provenance_store=store,
    ).execute(
        policy=policy,
        activated_by="runtime",
    )

    return store.get_active_policy()


def rollback_core_runtime_calibration() -> RuntimeCalibrationPolicy:
    store = _core_lifecycle_store()

    return RollbackRuntimeCalibrationUseCase(
        activation_store=store,
        rollback_store=store,
        provenance_store=store,
    ).execute(
        reason_code="CALIBRATION_RUNTIME_ROLLBACK",
        rolled_back_by="runtime",
    )


def get_core_calibration_provenance() -> list[dict[str, str]]:
    return _core_lifecycle_store().list_events()


def _load_verified_core_policy() -> RuntimeCalibrationPolicy:
    use_case = LoadRuntimeCalibrationUseCase(
        reader=FileCalibrationPolicyReader(settings.core_calibration_policy_path),
        integrity_verifier=Sha256CalibrationIntegrityVerifier(),
        signature_verifier=Ed25519CalibrationSignatureVerifier(
            settings.core_calibration_public_key_b64
        ),
        manifest=FileCalibrationManifestReader(settings.core_calibration_manifest_path).read(),
        trusted_registry=FileTrustedCalibrationRegistryReader(
            settings.core_calibration_registry_path
        ).read(),
    )

    return use_case.execute(
        expected_service="core",
        expected_contract_version=project_metadata.contract_version,
        expected_model_identifier=settings.age_model_id,
    )


def _core_lifecycle_store() -> FileCalibrationLifecycleStore:
    return FileCalibrationLifecycleStore(settings.core_calibration_state_dir)
