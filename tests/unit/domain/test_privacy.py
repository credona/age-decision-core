from app.domain.privacy import PrivacyMetadataBuilder


def test_privacy_metadata_is_ephemeral():
    builder = PrivacyMetadataBuilder()

    result = builder.build(zk_ready=True)

    assert result["image_stored"] is False
    assert result["biometric_template_stored"] is False
    assert result["processing"] == "ephemeral"
    assert result["zk_ready"] is True