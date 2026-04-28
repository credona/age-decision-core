import os

os.environ["USE_MOCK_MODEL"] = "true"

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def fake_image_bytes():
    # Minimal invalid image bytes are not enough for /estimate because image decoding is tested.
    # Endpoint tests that need image decoding should mock the estimator instead.
    return b"fake-image-content"
