from app.infrastructure.config.settings import Settings


def test_settings_expose_runtime_model_configuration() -> None:
    settings = Settings()

    assert settings.age_model_id
    assert settings.age_model_version
    assert settings.age_scoring_policy_id
    assert settings.face_detection_model_id
    assert settings.face_detection_model_version


def test_settings_expose_runtime_privacy_configuration() -> None:
    settings = Settings()

    assert settings.privacy_mode is True
    assert settings.enable_zk_ready is True


def test_settings_expose_runtime_calibration_configuration() -> None:
    settings = Settings()

    assert settings.core_calibration_policy_path is None
    assert settings.core_calibration_public_key_b64 is None
    assert settings.core_calibration_required is False
