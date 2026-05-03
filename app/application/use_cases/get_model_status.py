from app.application.use_cases.decision_pipeline import DecisionPipeline


class GetEngineStatusUseCase:
    """
    Application use case for model status retrieval.
    """

    def __init__(self, service: DecisionPipeline):
        self.service = service

    def execute(self) -> dict:
        return self.service.get_engine_status()
