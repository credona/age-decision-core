from app.application.dto.estimate_command import EstimateCommand
from app.application.use_cases.age_estimation_pipeline import AgeEstimationService


class EstimateAgeDecisionUseCase:
    """
    Application use case for age decision estimation.

    This layer receives framework-neutral input data and orchestrates the
    internal age decision pipeline. Public response filtering remains in API.
    """

    def __init__(self, service: AgeEstimationService):
        self.service = service

    async def execute(self, command: EstimateCommand) -> dict:
        return await self.service.estimate(
            image_bytes=command.image_bytes,
            content_type=command.content_type,
            request_id=command.request_id,
            correlation_id=command.correlation_id,
            age_threshold=command.age_threshold,
            majority_country=command.majority_country,
        )
