from app.application.use_cases.decision_pipeline import DecisionPipeline


class FakeInferenceEngine:
    def get_status(self) -> dict:
        return {
            "model_id": "credona.age.test.v1",
            "model_version": "1.0.0",
            "task": "age_estimation",
            "runtime": "mock",
            "scoring_policy_id": "credona.age.threshold-margin.v1",
        }

    def predict(self, prepared_input):
        return 25.0, 0.9


class FakeInputAnalyzer:
    def get_status(self) -> dict:
        return {
            "engine": "fake-face-detector",
            "loaded": True,
        }

    def detect(self, image):
        return []


class FakeImageDecoder:
    def decode(self, image_bytes: bytes):
        return object()


class FakeFaceCropper:
    def crop(self, image, faces):
        return object()


class FakeInputPreprocessor:
    def preprocess(self, face_image):
        return object()


def test_engine_status_uses_public_contract_keys() -> None:
    pipeline = DecisionPipeline(
        inference_engine=FakeInferenceEngine(),
        input_analyzer=FakeInputAnalyzer(),
        image_decoder=FakeImageDecoder(),
        face_cropper=FakeFaceCropper(),
        input_preprocessor=FakeInputPreprocessor(),
    )

    status = pipeline.get_engine_status()

    assert set(status) == {"input_analysis", "inference"}
    assert "face_detection" not in status
    assert "age_estimation" not in status
