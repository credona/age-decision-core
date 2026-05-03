from typing import Protocol

from app.domain.models.metadata import ModelMetadata


class ModelRegistryPort(Protocol):
    def get(self, model_id: str) -> ModelMetadata: ...

    def validate(self) -> None: ...
