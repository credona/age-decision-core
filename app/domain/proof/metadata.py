from app.domain.decision.constants import (
    PROOF_CLAIM_AGE_OVER_THRESHOLD,
    PROOF_STATUS_DISABLED,
    PROOF_STATUS_NOT_GENERATED,
    PROOF_TYPE_NONE,
    PROOF_TYPE_ZK_READY,
)


class ProofMetadataBuilder:
    """
    Builds ZK-ready proof metadata.

    This does not generate a real Zero Knowledge proof.
    It prepares the response contract for a future proof system.
    """

    def build(
        self,
        enabled: bool,
        threshold: dict,
    ) -> dict:
        if not enabled:
            return {
                "type": PROOF_TYPE_NONE,
                "status": PROOF_STATUS_DISABLED,
                "claim": None,
                "threshold": threshold,
            }

        return {
            "type": PROOF_TYPE_ZK_READY,
            "status": PROOF_STATUS_NOT_GENERATED,
            "claim": PROOF_CLAIM_AGE_OVER_THRESHOLD,
            "threshold": threshold,
        }
