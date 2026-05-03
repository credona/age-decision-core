def test_openapi_estimate_schema_contains_v2_privacy_first_fields(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    schema = payload["components"]["schemas"]["DecisionResponse"]
    properties = schema["properties"]

    assert "decision" in properties
    assert "threshold" in properties
    assert "cred_decision_score" in properties
    assert "privacy" in properties
    assert "proof" in properties

    assert "internal_estimate" not in properties
    assert "signal_quality_score" not in properties
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


def test_openapi_error_response_schema_exposes_only_standardized_fields(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    schema = payload["components"]["schemas"]["ErrorResponse"]
    properties = schema["properties"]

    assert set(properties.keys()) == {"request_id", "correlation_id", "error"}


def test_openapi_error_detail_schema_exposes_only_standardized_fields(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    schema = payload["components"]["schemas"]["ErrorDetail"]
    properties = schema["properties"]

    assert set(properties.keys()) == {"code", "message"}
