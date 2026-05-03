from pathlib import Path

from app.domain.models.metadata import ModelMetadata


class ModelLoader:
    """
    Loads ONNX models from disk using validated model metadata.
    """

    def __init__(self, model: ModelMetadata, use_mock: bool = False):
        self.model = model
        self.use_mock = use_mock
        self.session = None

    def load(self):
        if self.use_mock:
            return None

        if not Path(self.model.path).exists():
            raise RuntimeError("Configured model file was not found.")

        try:
            import onnxruntime as ort

            self.session = ort.InferenceSession(
                self.model.path,
                providers=["CPUExecutionProvider"],
            )

            return self.session

        except Exception as exc:
            raise RuntimeError("Failed to load configured ONNX model.") from exc
