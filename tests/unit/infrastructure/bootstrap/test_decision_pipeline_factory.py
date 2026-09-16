from unittest.mock import patch

from app.application.ports.scientific_observer import NullScientificObserver
from app.infrastructure.bootstrap.decision_pipeline import build_decision_pipeline


class RecordingScientificObserver:
    def observe_age_inference(
        self,
        *,
        internal_estimate: float,
        signal_quality_score: float,
    ) -> None:
        pass


def build_with_mocked_adapters(scientific_observer=None):
    with (
        patch(
            "app.infrastructure.bootstrap.decision_pipeline.OnnxInferenceEngine"
        ) as inference_engine,
        patch(
            "app.infrastructure.bootstrap.decision_pipeline.OpenCvInputAnalyzer"
        ) as input_analyzer,
        patch("app.infrastructure.bootstrap.decision_pipeline.OpenCvImageDecoder") as image_decoder,
        patch("app.infrastructure.bootstrap.decision_pipeline.FaceCropper") as face_cropper,
        patch(
            "app.infrastructure.bootstrap.decision_pipeline.FacePreprocessor"
        ) as input_preprocessor,
        patch("app.infrastructure.bootstrap.decision_pipeline.SafeEventLogger") as event_logger,
    ):
        pipeline = build_decision_pipeline(
            scientific_observer=scientific_observer,
        )

        assert pipeline.inference_engine is inference_engine.return_value
        assert pipeline.input_analyzer is input_analyzer.return_value
        assert pipeline.image_decoder is image_decoder.return_value
        assert pipeline.face_cropper is face_cropper.return_value
        assert pipeline.input_preprocessor is input_preprocessor.return_value
        assert pipeline.event_logger is event_logger.return_value

        return pipeline


def test_factory_uses_null_scientific_observer_by_default() -> None:
    pipeline = build_with_mocked_adapters()

    assert isinstance(
        pipeline.scientific_observer,
        NullScientificObserver,
    )


def test_factory_preserves_explicit_scientific_observer() -> None:
    observer = RecordingScientificObserver()

    pipeline = build_with_mocked_adapters(
        scientific_observer=observer,
    )

    assert pipeline.scientific_observer is observer
