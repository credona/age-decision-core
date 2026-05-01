from app.application.use_cases.age_estimation_pipeline import AgeEstimationService


class GetModelStatusUseCase:
    """
    Application use case for model status retrieval.
    """

    def __init__(self, service: AgeEstimationService):
        self.service = service

    def execute(self) -> dict:
        return self.service.get_model_status()
