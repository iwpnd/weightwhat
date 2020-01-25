import json
import pytest
from weightwhat.api.api_v1 import crud
from weightwhat.core.config import API_PREFIX


def test_create_weight(test_app, monkeypatch):
    test_request_payload = {"weight": 88.1}
    test_response_payload = {
        "id": 1,
        "weight": test_request_payload["weight"],
        "created_at": "1970-01-01 13:37:00",
    }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        API_PREFIX + "/weight", data=json.dumps(test_request_payload)
    )

    assert response.status_code == 201
    assert all([k in response.json() for k in test_response_payload.keys()])


def test_create_weight_invalid_json(test_app):
    response = test_app.post(
        API_PREFIX + "/weight", data=json.dumps({"weight": "achtundsiebzigkommadrei"})
    )
    assert response.status_code == 422
