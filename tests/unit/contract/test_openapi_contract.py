def test_openapi_estimate_schema_contains_score_fields(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    schema = payload["components"]["schemas"]["AgeDecisionResponse"]
    properties = schema["properties"]

    assert "cred_decision_score" in properties
    assert "cred_score" in properties


def test_openapi_estimate_declares_error_responses(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    estimate = payload["paths"]["/estimate"]["post"]
    responses = estimate["responses"]

    assert "400" in responses
    assert "500" in responses