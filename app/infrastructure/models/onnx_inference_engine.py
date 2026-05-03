import numpy as np

from app.infrastructure.config.settings import settings
from app.infrastructure.models.model_loader import ModelLoader
from app.infrastructure.models.registry import build_default_model_registry


class OnnxInferenceEngine:
    """
    Runs the configured ONNX inference engine through a deterministic model registry.
    """

    def __init__(self):
        self.use_mock = settings.use_mock_model
        self.registry = build_default_model_registry()
        self.model = self.registry.get(settings.age_model_id)

        self.model_loader = ModelLoader(
            model=self.model,
            use_mock=self.use_mock,
        )

        self.session = self.model_loader.load()

    def get_status(self) -> dict:
        base_status = {
            "model_id": self.model.model_id,
            "model_version": self.model.model_version,
            "task": self.model.task,
            "runtime": self.model.runtime,
            "scoring_policy_id": self.model.scoring_policy_id,
        }

        if self.use_mock or self.session is None:
            return {
                **base_status,
                "mode": "mock",
                "use_mock_model": self.use_mock,
                "model_loaded": False,
                "output_supported": True,
            }

        return {
            **base_status,
            "mode": "onnx",
            "use_mock_model": self.use_mock,
            "model_loaded": True,
            "output_supported": self._has_supported_age_output(),
        }

    def predict(self, prepared_input: np.ndarray) -> tuple[float, float]:
        if self.use_mock or self.session is None:
            return 25.0, settings.default_signal_quality

        if not self._has_supported_age_output():
            raise RuntimeError("Configured ONNX model does not expose a supported output.")

        return self._onnx_prediction(prepared_input)

    def _has_supported_age_output(self) -> bool:
        if self.session is None:
            return False

        for output in self.session.get_outputs():
            shape = output.shape

            if len(shape) != 2:
                continue

            last_dim = shape[1]

            if last_dim in {1, 2}:
                return True

            if isinstance(last_dim, int) and last_dim >= 80:
                return True

        return False

    def _onnx_prediction(self, prepared_input: np.ndarray) -> tuple[float, float]:
        input_name = self.session.get_inputs()[0].name
        outputs = self.session.run(None, {input_name: prepared_input})

        age, signal_quality_score = self._parse_outputs(outputs)

        if age < 0 or age > 120:
            raise RuntimeError("Invalid internal estimate returned by inference engine.")

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
            return float(age), settings.default_signal_quality

        if logits.shape[1] == 1:
            age = float(logits[0][0])
            return age, settings.default_signal_quality

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
