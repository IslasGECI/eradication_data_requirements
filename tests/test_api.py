from eradication_data_requirements import api
from fastapi.testclient import TestClient
import geci_test_tools as gtt
import json

client = TestClient(api)


def tests_api_filter_by_method():
    input_path = "tests/data/terrestrial_hunting.csv"
    output_path = "tests/data/filtered_by_tecnique.csv"
    method = "Cacería terrestre"

    gtt.if_exist_remove(output_path)

    request = f"/filer_by_method/?input_path={input_path}&method={method}&output_path={output_path}"
    response = client.get(request)
    assert response.status_code == 200


def tests_api_write_population_status():
    input_path = "tests/data/erradicacion_cabras_maria_cleofas.csv"
    bootstrapping_number = 100
    output_path = "tests/data/population_status.json"

    gtt.if_exist_remove(output_path)

    request = f"/write_population_status/?input_path={input_path}&bootstrapping_number={bootstrapping_number}&output_path={output_path}"
    response = client.get(request)
    assert response.status_code == 200
    gtt.assert_exist(output_path)
    with open(output_path) as json_file:
        data = json.load(json_file)
    assert "remanentes" in data.keys()


def tests_api_write_effort_and_captures_with_probability():
    input_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    bootstrapping_number = 10
    output_path = "tests/data/api_effort_captures_probability.csv"

    gtt.if_exist_remove(output_path)

    window_length = 6
    request = f"/write_effort_and_captures_with_probability/?input_path={input_path}&bootstrapping_number={bootstrapping_number}&output_path={output_path}&window_length={window_length}"
    response = client.get(request)
    assert response.status_code == 200

    gtt.assert_exist(output_path)
    gtt.if_exist_remove(output_path)


def tests_api_write_progress_probability_figure():
    input_path = "tests/data/progress_probability_tests.csv"
    output_path = "tests/data/api_reggae_figure.png"

    gtt.if_exist_remove(output_path)

    request = f"/write_probability_figure/?input_path={input_path}&output_path={output_path}"
    response = client.get(request)
    assert response.status_code == 200

    gtt.assert_exist(output_path)
    gtt.if_exist_remove(output_path)


def tests_plot_cumulative_series_cpue_by_flight():
    input_path = "tests/data/feral_goat_capture_effort.csv"
    output_path = "tests/data/flight_cpue_series.png"

    gtt.if_exist_remove(output_path)

    request = (
        f"/plot_cumulative_series_cpue_by_flight/?input_path={input_path}&output_path={output_path}"
    )
    response = client.get(request)
    assert response.status_code == 200

    gtt.assert_exist(output_path)
    gtt.if_exist_remove(output_path)


def tests_api_plot_cpue_vs_cum_captures():
    input_path = "tests/data/cumulative_effort_and_captures_for_year.csv"
    output_path = "tests/data/cpue_vs_cumulative.png"

    gtt.if_exist_remove(output_path)

    request = f"/plot_cpue_vs_cum_captures/?input_path={input_path}&output_path={output_path}"
    response = client.get(request)
    assert response.status_code == 200

    gtt.assert_exist(output_path)
    gtt.if_exist_remove(output_path)


def tests_api_plot_custom_cpue_vs_cum_captures():
    input_path = "tests/data/erradicacion_cabras_maria_cleofas.csv"
    config_path = "tests/data/hunt_config.json"
    output_path = "tests/data/cpue_vs_cumulative_from_config.png"

    gtt.if_exist_remove(output_path)

    request = f"/plot_custom_cpue_vs_cum_captures/?input_path={input_path}&config_path={config_path}&output_path={output_path}"
    response = client.get(request)
    assert response.status_code == 200

    gtt.assert_exist(output_path)
    gtt.if_exist_remove(output_path)


def tests_plot_comparative_catch_curves():
    socorro_path = "tests/data/cumulative_effort_and_captures_for_year.csv"
    guadalupe_path = "tests/data/cumulative_effort_and_captures_for_year_guadalupe.csv"
    output_path = "tests/data/comparative_catch_curves.png"

    gtt.if_exist_remove(output_path)

    request = f"/plot_comparative_catch_curves/?socorro_path={socorro_path}&guadalupe_path={guadalupe_path}&output_path={output_path}"
    response = client.get(request)
    assert response.status_code == 200
    gtt.assert_exist(output_path)
    gtt.if_exist_remove(output_path)
