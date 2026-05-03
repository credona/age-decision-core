from app.domain.decision.constants import PROCESSING_EPHEMERAL


class PrivacyMetadataBuilder:
    """
    Builds privacy metadata for the response.

    The core must not store raw images, biometric templates, or base64 payloads.
    Internal estimates are used only during computation and must not be exposed publicly.
    """

    def build(self, zk_ready: bool) -> dict:
        return {
            "image_stored": False,
            "biometric_template_stored": False,
            "internal_estimate_exposed": False,
            "processing": PROCESSING_EPHEMERAL,
            "zk_ready": zk_ready,
        }
