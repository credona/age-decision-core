import numpy as np

from app.infrastructure.config.settings import settings
from app.infrastructure.models.model_loader import ModelLoader


class OnnxInferenceEngine:
    """
    Runs the configured ONNX inference engine.
    """

    def __init__(self):
        self.use_mock = settings.use_mock_model

        self.model_loader = ModelLoader(
            model_path=settings.age_model_path,
            use_mock=self.use_mock,
        )

        self.session = self.model_loader.load()

    def get_status(self) -> dict:
        if self.use_mock or self.session is None:
            return {
                "mode": "mock",
                "use_mock_model": self.use_mock,
                "model_loaded": False,
                "output_supported": True,
            }

        return {
            "mode": "onnx",
            "use_mock_model": self.use_mock,
            "model_loaded": True,
            "output_supported": self._has_supported_age_output(),
            "inputs": [
                {
                    "name": input_.name,
                    "shape": input_.shape,
                    "type": input_.type,
                }
                for input_ in self.session.get_inputs()
            ],
            "outputs": [
                {
                    "name": output.name,
                    "shape": output.shape,
                    "type": output.type,
                }
                for output in self.session.get_outputs()
            ],
        }

    def predict(self, prepared_input: np.ndarray) -> tuple[float, float]:
        """
        Run inference and return (internal_estimate, signal_quality_score).
        """
        if self.use_mock or self.session is None:
            return 25.0, settings.default_signal_quality

        if not self._has_supported_age_output():
            raise RuntimeError("Configured ONNX model does not expose a supported output.")

        return self._onnx_prediction(prepared_input)

    def _has_supported_age_output(self) -> bool:
        """
        Supported outputs:
        - age-gender model: [batch, 2], where logits[0][0] is age
        - direct regression: [batch, 1]
        - age distribution: [batch, >=80]
        """
        if self.session is None:
            return False

        for output in self.session.get_outputs():
            shape = output.shape

            if len(shape) != 2:
                continue

            last_dim = shape[1]

            if last_dim == 2:
                return True

            if last_dim == 1:
                return True

            if isinstance(last_dim, int) and last_dim >= 80:
                return True

        return False

    def _onnx_prediction(self, prepared_input: np.ndarray) -> tuple[float, float]:
        input_name = self.session.get_inputs()[0].name

        outputs = self.session.run(None, {input_name: prepared_input})

        age, signal_quality_score = self._parse_outputs(outputs)

        if age < 0 or age > 120:
            raise RuntimeError(f"Invalid internal estimate returned by inference engine: {age}")

        if signal_quality_score < 0 or signal_quality_score > 1:
            raise RuntimeError("Invalid signal quality score returned by inference engine.")

        return age, signal_quality_score

    def _parse_outputs(self, outputs) -> tuple[float, float]:
        logits = np.asarray(outputs[0])

        if logits.ndim != 2:
            raise RuntimeError("Unsupported inference output format.")

        if logits.shape[1] == 2:
            age_logit = float(logits[0][0])
            age = min(max(round(age_logit), 0), 100)

            # The current age-gender ONNX model does not expose direct direct signal quality score.
            signal_quality_score = settings.default_signal_quality

            return float(age), signal_quality_score

        if logits.shape[1] == 1:
            age = float(logits[0][0])
            signal_quality_score = settings.default_signal_quality

            return age, signal_quality_score

        if logits.shape[1] >= 80:
            values = logits[0]
            probabilities = self._softmax_if_needed(values)
            ages = np.arange(probabilities.size)

            age = float(np.sum(probabilities * ages))
            signal_quality_score = float(np.max(probabilities))

            return age, signal_quality_score

        raise RuntimeError("Unsupported inference output format.")

    def _softmax_if_needed(self, values: np.ndarray) -> np.ndarray:
        total = float(np.sum(values))

        if np.all(values >= 0) and 0.99 <= total <= 1.01:
            return values.astype(np.float32)

        shifted = values - np.max(values)
        exp_values = np.exp(shifted)

        return (exp_values / np.sum(exp_values)).astype(np.float32)
