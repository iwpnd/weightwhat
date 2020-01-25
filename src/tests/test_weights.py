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


def test_get_weight_by_id(test_app, monkeypatch):
    test_data = {
        "created_at": "2020-10-10T10:10:10",
        "id": 1,
        "updated_at": "2020-10-10T10:10:10",
        "weight": 100.0,
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(API_PREFIX + "/weight/1")

    assert response.status_code == 200
    assert response.json() == test_data


def test_get_weight_by_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(API_PREFIX + "/weight/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "weight id not found"
