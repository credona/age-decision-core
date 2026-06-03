from app.application.calibration.ports import (
    CalibrationActivationStorePort,
    CalibrationProvenanceStorePort,
)
from app.domain.calibration import CalibrationActivationRecord, RuntimeCalibrationPolicy


class ActivateRuntimeCalibrationUseCase:
    def __init__(
        self,
        activation_store: CalibrationActivationStorePort,
        provenance_store: CalibrationProvenanceStorePort,
    ):
        self.activation_store = activation_store
        self.provenance_store = provenance_store

    def execute(
        self,
        *,
        policy: RuntimeCalibrationPolicy,
        activated_by: str = "runtime",
    ) -> CalibrationActivationRecord:
        record = CalibrationActivationRecord.create(
            policy_id=policy.metadata.policy_id,
            policy_version=policy.metadata.policy_version,
            benchmark_attestation_id=policy.metadata.benchmark_attestation_id,
            model_identifier=policy.metadata.model_identifier,
            activated_by=activated_by,
        )

        self.activation_store.set_active_policy(policy, record)
        self.provenance_store.append(record)

        return record
