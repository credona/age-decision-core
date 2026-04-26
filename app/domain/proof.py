class ProofMetadataBuilder:
    """
    Builds ZK-ready proof metadata.

    This does not generate a real Zero Knowledge proof.
    It only prepares the response contract for a future proof system.
    """

    def build(
        self,
        enabled: bool,
        threshold: int,
    ) -> dict:
        if not enabled:
            return {
                "type": "none",
                "status": "disabled",
                "claim": None,
                "threshold": threshold,
            }

        return {
            "type": "zk-ready",
            "status": "not_generated",
            "claim": "age_over_threshold",
            "threshold": threshold,
        }