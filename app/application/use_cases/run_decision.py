from app.application.dto.estimate_command import EstimateCommand
from app.application.use_cases.decision_pipeline import DecisionPipeline


class RunDecisionUseCase:
    """
    Application use case for decision execution.

    This layer receives framework-neutral input data and orchestrates the
    internal decision pipeline. Public response filtering remains in API.
    """

    def __init__(self, service: DecisionPipeline):
        self.service = service

    async def execute(self, command: EstimateCommand) -> dict:
        return await self.service.run(
            image_bytes=command.image_bytes,
            content_type=command.content_type,
            request_id=command.request_id,
            correlation_id=command.correlation_id,
            age_threshold=command.age_threshold,
            majority_country=command.majority_country,
        )
