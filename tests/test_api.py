from eradication_data_requirements import api
from fastapi.testclient import TestClient
import io
import pandas as pd

client = TestClient(api)


def tests_api_write_bootstrap_progress_intervals_json():
    input_path = "tests/data/erradicacion_cabras_maria_cleofas.csv"
    bootstrapping_number = 10

    with open(input_path, "rb") as f:
        input_file_like = io.BytesIO(f.read())
    request = {
        "url": "/write_bootstrap_progress_intervals_json",
        "files": {
            "input_path": (input_path, input_file_like, "text/csv"),
        },
        "data": {"bootstrapping_number": bootstrapping_number},
    }
    response = client.post(**request)
    assert response.status_code == 200

    content = response.json()
    assert "intervals" in content


def tests_api_write_aerial_monitoring():
    input_path = "tests/data/monitoreo_cabras_magdalena.csv"
    bootstrapping_number = 10

    with open(input_path, "rb") as f:
        input_file_like = io.BytesIO(f.read())

    request = {
        "url": "/write_aerial_monitoring",
        "files": {
            "input_path": (input_path, input_file_like, "text/csv"),
        },
        "data": {"bootstrapping_number": bootstrapping_number},
    }
    response = client.post(**request)
    assert response.status_code == 200

    content = response.json()
    assert "total" in content.keys()


def tests_api_filter_by_method():
    input_path = "tests/data/terrestrial_hunting.csv"
    method = "Cacería terrestre"

    with open(input_path, "rb") as f:
        input_file_like = io.BytesIO(f.read())
    request = {
        "url": "/filter_by_method",
        "files": {
            "input_path": (input_path, input_file_like, "text/csv"),
        },
        "data": {"method": method},
    }
    response = client.post(**request)
    assert response.status_code == 200

    content = response.json()
    obtained = pd.DataFrame(content)
    assert obtained.shape[1] == 9


def tests_api_write_population_status_from_mixed_methods():
    first_method_path = "tests/data/population_status_terrestrial_hunting.json"
    second_method_path = "tests/data/population_status_aerial_hunting.json"

    with open(first_method_path, "rb") as f:
        file_like_first_method = io.BytesIO(f.read())
    with open(second_method_path, "rb") as f:
        file_like_second_method = io.BytesIO(f.read())

    request = {
        "url": "/write_population_status_from_mixed_methods",
        "files": {
            "first_method_status": (first_method_path, file_like_first_method, "application/json"),
            "second_method_status": (
                second_method_path,
                file_like_second_method,
                "application/json",
            ),
        },
    }

    response = client.post(**request)
    assert response.status_code == 200
    content = response.json()
    assert "remanentes" in content
    assert "capturas" in content
    assert "remanentes_distribution" in content


def tests_api_write_population_status():
    input_path = "tests/data/erradicacion_cabras_maria_cleofas.csv"
    bootstrapping_number = 100

    with open(input_path, "rb") as f:
        file_like = io.BytesIO(f.read())

    request = {
        "url": "/write_population_status",
        "files": {"file": ("data.csv", file_like, "text/csv")},
        "data": {"bootstrapping_number": bootstrapping_number},
    }

    response = client.post(**request)
    assert response.status_code == 200
    content = response.json()
    assert "n0" in content
    assert "remanentes" in content.keys()


def tests_api_write_effort_and_captures_with_probability():
    input_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    bootstrapping_number = 10
    window_length = 6

    with open(input_path, "rb") as f:
        file_like = io.BytesIO(f.read())

    request = {
        "url": "/write_effort_and_captures_with_probability",
        "files": {"file": ("data.csv", file_like, "text/csv")},
        "data": {"bootstrapping_number": bootstrapping_number, "window_length": window_length},
    }
    response = client.post(**request)
    assert response.status_code == 200

    content = response.json()
    assert isinstance(content, list)
    assert len(content) > 0
    assert "Esfuerzo" in content[0]
    assert "Capturas" in content[0]
    assert "Fecha" in content[0]
    assert "prob" in content[0]

    resolution = 7
    request = {
        "url": "/write_effort_and_captures_with_probability",
        "files": {"file": ("data.csv", file_like, "text/csv")},
        "data": {
            "bootstrapping_number": bootstrapping_number,
            "window_length": window_length,
            "resolution": resolution,
        },
    }
    response = client.post(**request)
    assert response.status_code == 200


def tests_api_write_progress_probability_figure():
    input_path = "tests/data/progress_probability_tests.csv"

    with open(input_path, "rb") as f:
        file_like = io.BytesIO(f.read())

    request = {
        "url": "/write_probability_figure",
        "files": {"file": ("data.csv", file_like, "text/csv")},
    }
    response = client.post(**request)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 10  # sanity check: PNGs should not be tiny


def tests_plot_cumulative_series_cpue_by_flight():
    input_path = "tests/data/feral_goat_capture_effort.csv"

    with open(input_path, "rb") as f:
        input_file_like = io.BytesIO(f.read())

    img_format = "eps"
    request = {
        "url": "/plot_cumulative_series_cpue_by_flight",
        "files": {
            "file": ("file.csv", input_file_like, "text/csv"),
        },
        "data": {"format": img_format},
    }

    response = client.post(**request)
    assert response.status_code == 200
    assert response.headers["content-type"] == f"image/{img_format}"
    minimum_empty_eps = 630
    assert len(response.content) > minimum_empty_eps


def tests_plot_cumulative_series_cpue_by_season():
    input_path = "tests/data/esfuerzo_capturas_gatos_guadalupe_ISO_for_tests.csv"

    with open(input_path, "rb") as f:
        input_file_like = io.BytesIO(f.read())

    img_format = "eps"
    request = {
        "url": "/plot_cumulative_series_cpue_by_season",
        "files": {
            "file": ("file.csv", input_file_like, "text/csv"),
        },
        "data": {"format": img_format},
    }

    response = client.post(**request)
    assert response.status_code == 200
    assert response.headers["content-type"] == f"image/{img_format}"
    minimum_empty_eps = 630
    assert len(response.content) > minimum_empty_eps


def tests_api_plot_cpue_vs_cum_captures():
    input_path = "tests/data/cumulative_effort_and_captures_for_year.csv"

    with open(input_path, "rb") as f:
        file_like = io.BytesIO(f.read())

    request = {
        "url": "/plot_cpue_vs_cum_captures",
        "files": {"file": ("data.csv", file_like, "text/csv")},
    }
    response = client.post(**request)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 10  # sanity check: PNGs should not be tiny

    format = "eps"
    request = {
        "url": "/plot_cpue_vs_cum_captures",
        "files": {"file": ("data.csv", file_like, "text/csv")},
        "data": {"format": format},
    }
    response = client.post(**request)
    assert response.status_code == 200
    assert response.headers["content-type"] == f"image/{format}"
    # sanity check: images should not be tiny
    assert len(response.content) > 10


def tests_api_plot_custom_cpue_vs_cum_captures():
    input_path = "tests/data/erradicacion_cabras_maria_cleofas.csv"
    config_path = "tests/data/hunt_config.json"

    with open(input_path, "rb") as f:
        file_like = io.BytesIO(f.read())
    with open(config_path, "rb") as f:
        config_like = io.BytesIO(f.read())

    format = "eps"
    request = {
        "url": "/plot_custom_cpue_vs_cum_captures",
        "files": {
            "file": ("data.csv", file_like, "text/csv"),
            "config": ("config.json", config_like, "application/json"),
        },
        "data": {"format": format},
    }

    response = client.post(**request)
    assert response.status_code == 200
    assert response.headers["content-type"] == f"image/{format}"
    assert len(response.content) > 10


def tests_plot_comparative_catch_curves():
    socorro_path = "tests/data/cumulative_effort_and_captures_for_year.csv"
    guadalupe_path = "tests/data/cumulative_effort_and_captures_for_year_guadalupe.csv"

    with open(socorro_path, "rb") as f:
        socorro_file_like = io.BytesIO(f.read())
    with open(guadalupe_path, "rb") as f:
        guadalupe_file_like = io.BytesIO(f.read())

    format = "png"
    request = {
        "url": "/plot_comparative_catch_curves",
        "files": {
            "socorro_file": ("data_socorro.csv", socorro_file_like, "text/csv"),
            "guadalupe_file": ("data_guadalupe.csv", guadalupe_file_like, "text/csv"),
        },
    }

    response = client.post(**request)
    assert response.status_code == 200
    assert response.headers["content-type"] == f"image/{format}"
    assert len(response.content) > 10
    format = "eps"
    request = {
        "url": "/plot_comparative_catch_curves",
        "files": {
            "socorro_file": ("data_socorro.csv", socorro_file_like, "text/csv"),
            "guadalupe_file": ("data_guadalupe.csv", guadalupe_file_like, "text/csv"),
        },
        "data": {"format": format},
    }

    response = client.post(**request)
    assert response.status_code == 200
    assert response.headers["content-type"] == f"image/{format}"


def tests_plot_comparative_yearly_cpue():
    socorro_path = "tests/data/esfuerzo_capturas_gatos_guadalupe_ISO_for_tests.csv"
    guadalupe_path = "tests/data/esfuerzo_capturas_gatos_guadalupe_ISO_for_tests.csv"

    with open(socorro_path, "rb") as f:
        socorro_file_like = io.BytesIO(f.read())
    with open(guadalupe_path, "rb") as f:
        guadalupe_file_like = io.BytesIO(f.read())

    img_format = "eps"
    request = {
        "url": "/plot_comparative_yearly_cpue",
        "files": {
            "socorro_file": ("data_socorro.csv", socorro_file_like, "text/csv"),
            "guadalupe_file": ("data_guadalupe.csv", guadalupe_file_like, "text/csv"),
        },
        "data": {"format": img_format},
    }

    response = client.post(**request)
    assert response.status_code == 200
    assert response.headers["content-type"] == f"image/{img_format}"
    minimum_empty_eps = 630
    assert len(response.content) > minimum_empty_eps
