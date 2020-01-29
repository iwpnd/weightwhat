import json
from datetime import date

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


def test_get_weight_id_zero_invalid(test_app, monkeypatch):
    async def mock_get(id):
        return 0

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(API_PREFIX + "/weight/0")

    assert response.status_code == 422


def test_get_all_weights(test_app, monkeypatch):
    test_data = [
        {
            "created_at": "2020-10-10T10:10:10",
            "id": 1,
            "updated_at": "2020-10-10T10:10:10",
            "weight": 100.0,
        },
        {
            "created_at": "2020-10-07T10:10:10",
            "id": 2,
            "updated_at": "2020-10-07T10:10:10",
            "weight": 101.0,
        },
        {
            "created_at": "2020-10-05T10:10:10",
            "id": 3,
            "updated_at": "2020-10-05T10:10:10",
            "weight": 102.0,
        },
    ]

    async def mock_get_all(fromdate=None, todate=None):
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get(API_PREFIX + "/weights")

    assert response.status_code == 200
    assert response.json() == test_data


def test_get_all_weights_fails(test_app, monkeypatch):
    async def mock_get_all(fromdate=None, todate=None):
        return None

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get(API_PREFIX + "/weights")

    assert response.status_code == 404
    assert response.json()["detail"] == "no weights found"


def test_get_all_weights_from_to(test_app, monkeypatch):

    response_data = [
        {
            "created_at": "2020-10-07T10:10:10",
            "id": 2,
            "updated_at": "2020-10-07T10:10:10",
            "weight": 101.0,
        },
        {
            "created_at": "2020-10-05T10:10:10",
            "id": 3,
            "updated_at": "2020-10-05T10:10:10",
            "weight": 102.0,
        },
    ]

    async def mock_get_all_from_to(fromdate: str, todate: str):
        return response_data

    monkeypatch.setattr(crud, "get_all", mock_get_all_from_to)

    from_date = "2020-10-05"
    to_date = "2020-10-10"

    response = test_app.get(
        API_PREFIX + f"/weights", params={"fromdate": from_date, "todate": to_date}
    )

    assert response.status_code == 200
    assert response.json() == response_data


@pytest.mark.parametrize(
    "payload, status_code",
    [
        [{"fromdate": "foo", "todate": "bar"}, 422],
        [{"fromdate": 22, "todate": 20}, 404],
    ],
)
def test_get_all_weights_from_to_invalid(test_app, monkeypatch, payload, status_code):
    async def mock_get_all_from_to(fromdate: date, todate: date):
        return None

    monkeypatch.setattr(crud, "get_all", mock_get_all_from_to)

    response = test_app.get(
        API_PREFIX
        + f"""/weights?fromdate={payload["fromdate"]}&todate={payload["todate"]}"""
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {"weight": 100, "created_at": "2020-01-27T10:53:04"}, 200],
        [2, {"weight": 100}, 200],
    ],
)
def test_update_weight(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return [(1, 1, 1, 1)]

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(API_PREFIX + f"/weight/{id}", data=json.dumps(payload))

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [99999, {"weight": 101, "created_at": "2020-01-27T10:53:04"}, 404],
        [0, {"weight": 101, "created_at": "2020-01-27T10:53:04"}, 422],
    ],
)
def test_update_weight_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(API_PREFIX + f"/weight/{id}", data=json.dumps(payload))

    assert response.status_code == status_code


def test_remove_weight(test_app, monkeypatch):
    test_data = {"id": 1, "weight": 100}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)
    response = test_app.delete(API_PREFIX + "/weight/1")

    assert response.status_code == 200
    assert response.json() == test_data


@pytest.mark.parametrize("id, status_code", [[99999, 404], [0, 422]])
def test_remove_weight_incorrect_id(test_app, monkeypatch, id, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete(API_PREFIX + f"/weight/{id}")

    assert response.status_code == status_code


def test_get_weight_latest(test_app, monkeypatch):
    test_data = {
        "created_at": "2020-10-10T10:10:10",
        "id": 1,
        "updated_at": "2020-10-10T10:10:10",
        "weight": 100.0,
    }

    async def mock_get():
        return test_data

    monkeypatch.setattr(crud, "get_latest", mock_get)

    response = test_app.get(API_PREFIX + "/weight")

    assert response.status_code == 200
    assert response.json() == test_data


def test_get_weight_latest_fails(test_app, monkeypatch):
    async def mock_get():
        return None

    monkeypatch.setattr(crud, "get_latest", mock_get)

    response = test_app.get(API_PREFIX + "/weight")

    assert response.status_code == 404
    assert response.json()["detail"] == "no weights found"
