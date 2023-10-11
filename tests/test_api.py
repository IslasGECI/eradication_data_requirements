from eradication_data_requirements import api
from fastapi.testclient import TestClient
import os

client = TestClient(api)


def tests_api_write_effort_and_captures_with_probability():
    input_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    bootstrapping_number = 10
    output_path = "tests/data/api_effort_captures_probability.csv"

    if os.path.exists(output_path):
        os.remove(output_path)

    window_length = 6
    request = f"/write_effort_and_captures_with_probability/?input_path={input_path}&bootstrapping_number={bootstrapping_number}&output_path={output_path}&window_length={window_length}"
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
    os.remove(output_path)


def tests_api_plot_cpue_vs_cum_captures():
    input_path = "tests/data/cumulative_effort_and_captures_for_year.csv"
    output_path = "tests/data/cpue_vs_cumulative.png"

    if os.path.exists(output_path):
        os.remove(output_path)

    request = f"/plot_cpue_vs_cum_captures/?input_path={input_path}&output_path={output_path}"
    response = client.get(request)
    assert response.status_code == 200

    assert os.path.exists(output_path)
    os.remove(output_path)


def tests_plot_comparative_catch_curves():
    socorro_path = "tests/data/cumulative_effort_and_captures_for_year.csv"
    guadalupe_path = "tests/data/cumulative_effort_and_captures_for_year_guadalupe.csv"
    output_path = "tests/data/comparative_catch_curves.png"

    if os.path.exists(output_path):
        os.remove(output_path)

    request = f"/plot_comparative_catch_curves/?socorro_path={socorro_path}&guadalupe_path={guadalupe_path}&output_path={output_path}"
    response = client.get(request)
    assert response.status_code == 200

    assert os.path.exists(output_path)
    os.remove(output_path)
