def test_openapi_estimate_schema_contains_v2_privacy_first_fields(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    schema = payload["components"]["schemas"]["AgeDecisionResponse"]
    properties = schema["properties"]

    assert "decision" in properties
    assert "threshold" in properties
    assert "cred_decision_score" in properties
    assert "privacy" in properties
    assert "proof" in properties

    assert "estimated_age" not in properties
    assert "confidence" not in properties
    assert "is_adult" not in properties
    assert "cred_score" not in properties


def test_openapi_estimate_declares_error_responses(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    estimate = payload["paths"]["/estimate"]["post"]
    responses = estimate["responses"]

    assert "400" in responses
    assert "500" in responses
