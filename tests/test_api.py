from eradication_data_requirements import api
from fastapi.testclient import TestClient

client = TestClient(api)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def tests_api_write_effort_and_captures_with_probability():
    response = client.get("/write_effort_and_captures_with_probability")
    assert response.status_code == 200
