import pytest
from starlette.testclient import TestClient

from weightwhat.main import app


@pytest.fixture
def test_app():
    client = TestClient(app)
    yield client
