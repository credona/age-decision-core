from app.application.calibration.ports import CalibrationActivationStorePort


class GetPublicCalibrationSummaryUseCase:
    def __init__(self, activation_store: CalibrationActivationStorePort):
        self.activation_store = activation_store

    def execute(self) -> dict[str, str | bool] | None:
        from app.domain.calibration import PublicCalibrationSummary

        policy = self.activation_store.get_active_policy()

        if policy is None:
            return None

        return PublicCalibrationSummary.from_policy(
            policy,
            active=True,
        ).to_public_dict()
