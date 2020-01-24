from starlette.testclient import TestClient
import pytest

from weightwhat.main import app


@pytest.fixture
def test_app():
    client = TestClient(app)
    yield client
