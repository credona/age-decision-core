from io import BytesIO


def test_estimate_returns_stable_error_response_for_unsupported_file_type(client):
    response = client.post(
        "/estimate",
        headers={
            "X-Request-ID": "test-request-001",
            "X-Correlation-ID": "test-correlation-001",
        },
        files={
            "file": ("test.txt", BytesIO(b"not-an-image"), "text/plain"),
        },
    )

    assert response.status_code == 400

    payload = response.json()

    assert set(payload.keys()) == {"request_id", "correlation_id", "error"}
    assert set(payload["error"].keys()) == {"code", "message"}

    assert payload == {
        "request_id": "test-request-001",
        "correlation_id": "test-correlation-001",
        "error": {
            "code": "unsupported_file_type",
            "message": "Invalid request.",
        },
    }


def test_estimate_error_response_falls_back_to_request_id_as_correlation_id(client):
    response = client.post(
        "/estimate",
        headers={
            "X-Request-ID": "test-request-002",
        },
        files={
            "file": ("test.txt", BytesIO(b"not-an-image"), "text/plain"),
        },
    )

    assert response.status_code == 400

    payload = response.json()

    assert set(payload.keys()) == {"request_id", "correlation_id", "error"}
    assert set(payload["error"].keys()) == {"code", "message"}

    assert payload["request_id"] == "test-request-002"
    assert payload["correlation_id"] == "test-request-002"
    assert payload["error"]["code"] == "unsupported_file_type"
    assert payload["error"]["message"] == "Invalid request."


def test_estimate_missing_file_returns_stable_validation_error_shape(client):
    response = client.post(
        "/estimate",
        headers={
            "X-Request-ID": "test-request-003",
            "X-Correlation-ID": "test-correlation-003",
        },
    )

    assert response.status_code == 400

    payload = response.json()

    assert set(payload.keys()) == {"request_id", "correlation_id", "error"}
    assert set(payload["error"].keys()) == {"code", "message"}
    assert payload["request_id"] == "test-request-003"
    assert payload["correlation_id"] == "test-correlation-003"
    assert payload["error"]["code"] == "missing_file"
    assert payload["error"]["message"] == "Invalid request."


def test_estimate_missing_file_falls_back_to_request_id_as_correlation_id(client):
    response = client.post(
        "/estimate",
        headers={
            "X-Request-ID": "test-request-004",
        },
    )

    assert response.status_code == 400

    payload = response.json()

    assert payload["request_id"] == "test-request-004"
    assert payload["correlation_id"] == "test-request-004"
    assert payload["error"]["code"] == "missing_file"
    assert payload["error"]["message"] == "Invalid request."
