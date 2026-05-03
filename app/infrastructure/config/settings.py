from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    core_port: int = 8000

    age_model_id: str = "credona.age.age-gender-onnx.v1"
    age_model_version: str = "1.0.0"
    age_scoring_policy_id: str = "credona.age.threshold-margin.v1"

    face_detection_model_id: str = "credona.face.yunet.v1"
    face_detection_model_version: str = "1.0.0"

    face_detection_model_path: str = "models/face_detection/face_detection_yunet_2023mar.onnx"
    age_model_path: str = "models/age_estimation/age-gender-prediction-ONNX.onnx"

    use_mock_model: bool = False
    default_signal_quality: float = 0.8

    privacy_mode: bool = True
    enable_zk_ready: bool = True

    log_level: str = "INFO"
    log_format: str = "json"


settings = Settings()
