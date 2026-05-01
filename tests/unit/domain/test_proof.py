from app.domain.proof.metadata import ProofMetadataBuilder


def test_proof_metadata_enabled():
    builder = ProofMetadataBuilder()

    threshold = {
        "type": "minimum_age",
        "value": 18,
        "source": "majority_country",
        "majority_country": "FR",
    }

    result = builder.build(enabled=True, threshold=threshold)

    assert result["type"] == "zk-ready"
    assert result["status"] == "not_generated"
    assert result["claim"] == "age_over_threshold"
    assert result["threshold"] == threshold


def test_proof_metadata_disabled():
    builder = ProofMetadataBuilder()

    threshold = {
        "type": "minimum_age",
        "value": 18,
        "source": "default",
        "majority_country": None,
    }

    result = builder.build(enabled=False, threshold=threshold)

    assert result["type"] == "none"
    assert result["status"] == "disabled"
    assert result["threshold"] == threshold
