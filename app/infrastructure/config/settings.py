from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    core_port: int = 8000

    face_detection_model_path: str = "models/face_detection/face_detection_yunet_2023mar.onnx"
    age_model_path: str = "models/age_estimation/age-gender-prediction-ONNX.onnx"

    use_mock_model: bool = False
    default_signal_quality: float = 0.8

    age_threshold: int = 18
    age_margin: int = 2
    signal_quality_threshold: float = 0.7

    privacy_mode: bool = True
    enable_zk_ready: bool = True

    log_level: str = "INFO"
    log_format: str = "json"


settings = Settings()
