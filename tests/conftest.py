import pytest
from fastapi.testclient import TestClient

from fastapi_from_scratch.app import app


@pytest.fixture
def client():
    return TestClient(app)
