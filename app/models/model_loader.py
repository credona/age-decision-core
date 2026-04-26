import os


class ModelLoader:
    """
    Loads ONNX models from disk.
    """

    def __init__(self, model_path: str, use_mock: bool = False):
        self.model_path = model_path
        self.use_mock = use_mock
        self.session = None

    def load(self):
        """
        Load an ONNX model unless mock mode is enabled.
        """
        if self.use_mock:
            return None

        if not os.path.exists(self.model_path):
            raise RuntimeError(f"Model not found at path: {self.model_path}")

        try:
            import onnxruntime as ort

            self.session = ort.InferenceSession(
                self.model_path,
                providers=["CPUExecutionProvider"],
            )

            return self.session

        except Exception as exc:
            raise RuntimeError(f"Failed to load ONNX model: {exc}")