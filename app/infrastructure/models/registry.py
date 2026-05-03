from app.domain.models.metadata import ModelMetadata
from app.infrastructure.config.settings import settings


class StaticModelRegistry:
    def __init__(self, models: dict[str, ModelMetadata]):
        self.models = models
        self.validate()

    def get(self, model_id: str) -> ModelMetadata:
        try:
            return self.models[model_id]
        except KeyError as exc:
            raise ValueError("Unknown model identifier") from exc

    def validate(self) -> None:
        if not self.models:
            raise ValueError("Model registry must not be empty")

        for model in self.models.values():
            model.validate()


def build_default_model_registry() -> StaticModelRegistry:
    return StaticModelRegistry(
        models={
            settings.age_model_id: ModelMetadata(
                model_id=settings.age_model_id,
                model_version=settings.age_model_version,
                task="age_estimation",
                runtime="onnx",
                path=settings.age_model_path,
                scoring_policy_id=settings.age_scoring_policy_id,
                reproducibility={
                    "format": "onnx",
                    "execution_provider": "CPUExecutionProvider",
                },
            ),
            settings.face_detection_model_id: ModelMetadata(
                model_id=settings.face_detection_model_id,
                model_version=settings.face_detection_model_version,
                task="face_detection",
                runtime="onnx",
                path=settings.face_detection_model_path,
                scoring_policy_id="none",
                reproducibility={
                    "format": "onnx",
                    "execution_provider": "CPUExecutionProvider",
                },
            ),
        }
    )
