class PrivacyMetadataBuilder:
    """
    Builds privacy metadata for the response.

    The core must not store raw images, biometric templates, or base64 payloads.
    The estimated age is used internally and must not be exposed publicly.
    """

    def build(self, zk_ready: bool) -> dict:
        return {
            "image_stored": False,
            "biometric_template_stored": False,
            "estimated_age_exposed": False,
            "processing": "ephemeral",
            "zk_ready": zk_ready,
        }
