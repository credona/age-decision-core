class PrivacyMetadataBuilder:
    """
    Builds privacy metadata for the response.

    The core must not store raw images, biometric templates, or base64 payloads.
    Processing is expected to remain ephemeral.
    """

    def build(self, zk_ready: bool) -> dict:
        return {
            "image_stored": False,
            "biometric_template_stored": False,
            "processing": "ephemeral",
            "zk_ready": zk_ready,
        }