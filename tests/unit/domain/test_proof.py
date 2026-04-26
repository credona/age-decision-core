from app.domain.proof import ProofMetadataBuilder


def test_proof_metadata_enabled():
    builder = ProofMetadataBuilder()

    result = builder.build(enabled=True, threshold=18)

    assert result["type"] == "zk-ready"
    assert result["status"] == "not_generated"
    assert result["claim"] == "age_over_threshold"


def test_proof_metadata_disabled():
    builder = ProofMetadataBuilder()

    result = builder.build(enabled=False, threshold=18)

    assert result["type"] == "none"
    assert result["status"] == "disabled"