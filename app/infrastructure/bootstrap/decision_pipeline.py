from app.application.ports.scientific_observer import ScientificObserverPort
from app.application.use_cases.decision_pipeline import DecisionPipeline
from app.domain.calibration import RuntimeCalibrationPolicy
from app.infrastructure.logging.safe_event_logger import SafeEventLogger
from app.infrastructure.models.onnx_inference_engine import OnnxInferenceEngine
from app.infrastructure.vision.face_cropper import FaceCropper
from app.infrastructure.vision.face_preprocessor import FacePreprocessor
from app.infrastructure.vision.opencv_image_decoder import OpenCvImageDecoder
from app.infrastructure.vision.opencv_input_analyzer import OpenCvInputAnalyzer


def build_decision_pipeline(
    runtime_calibration: RuntimeCalibrationPolicy | None = None,
    scientific_observer: ScientificObserverPort | None = None,
) -> DecisionPipeline:
    """
    Build the production-equivalent Core decision pipeline.

    The scientific observer is an explicit private observation hook.
    Production callers leave it unset, which preserves the pipeline's
    no-op observer behavior.
    """
    return DecisionPipeline(
        inference_engine=OnnxInferenceEngine(),
        input_analyzer=OpenCvInputAnalyzer(),
        image_decoder=OpenCvImageDecoder(),
        face_cropper=FaceCropper(),
        input_preprocessor=FacePreprocessor(),
        event_logger=SafeEventLogger(),
        runtime_calibration=runtime_calibration,
        scientific_observer=scientific_observer,
    )
