from weightwhat.core.config import API_V1_STR


def test_ping(test_app):
    response = test_app.get(API_V1_STR + "/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}
