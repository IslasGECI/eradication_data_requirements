from eradication_data_requirements import api
from fastapi.testclient import TestClient
import os

client = TestClient(api)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def tests_api_write_effort_and_captures_with_probability():
    input_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    bootstrapping_number = 10
    output_path = "tests/data/api_effort_captures_probability.csv"

    if os.path.exists(output_path):
        os.remove(output_path)

    request = f"/write_effort_and_captures_with_probability/?input_path={input_path}&bootstrapping_number={bootstrapping_number}&output_path={output_path}"
    response = client.get(request)
    assert response.status_code == 200

    assert os.path.exists(output_path)
    os.remove(output_path)


def tests_api_write_progress_probability_figure():
    input_path = "tests/data/progress_probability_tests.csv"
    output_path = "tests/data/api_reggae_figure.png"

    if os.path.exists(output_path):
        os.remove(output_path)

    request = f"/write_probability_figure/?input_path={input_path}&output_path={output_path}"
    response = client.get(request)
    assert response.status_code == 200

    assert os.path.exists(output_path)
