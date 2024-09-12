import os
import hashlib
import pandas as pd
import numpy as np
import pytest

import eradication_data_requirements as dt

import matplotlib as mpl


def test_plot_comparative_catch_curves():
    socorro_path = "/workdir/tests/data/cumulative_effort_and_captures_for_year.csv"
    guadalupe_path = "/workdir/tests/data/cumulative_effort_and_captures_for_year_guadalupe.csv"
    output_path = "/workdir/tests/data/plot_comparative_catch_curves.png"
    remove_file_if_exists(output_path)
    dt.plot_comparative_catch_curves(socorro_path, guadalupe_path, output_path)
    file_content = open(output_path, "rb").read()
    obtained_hash = hashlib.md5(file_content).hexdigest()
    expected_hash = "8a0a4f88b8a99008e4a413474fca309b"
    assert obtained_hash == expected_hash
    remove_file_if_exists(output_path)


def test_data_requirements_plot():
    input_path = "/workdir/tests/data/cumulative_effort_and_captures_for_year.csv"
    output_path = "/workdir/tests/data/yearly_ramsey_plot.png"
    remove_file_if_exists(output_path)
    dt.traps_data_requirements_plot(input_path, output_path)
    file_content = open(output_path, "rb").read()
    obtained_hash = hashlib.md5(file_content).hexdigest()
    expected_hash = "ecaf873aba12424683a7e0fe15b2ea13"
    assert obtained_hash == expected_hash
    remove_file_if_exists(output_path)


def test_goat_data_requirement_plot():
    input_path = "/workdir/tests/data/erradicacion_cabras_maria_cleofas.csv"
    output_path = "/workdir/tests/data/goat_ramsey_plot.png"
    config_path = "/workdir/tests/data/hunt_config.json"
    remove_file_if_exists(output_path)
    obtained_plot = dt.plot_data_requirements_from_config_file(input_path, output_path, config_path)
    assert os.path.exists(output_path)
    assert isinstance(obtained_plot, mpl.axes._axes.Axes)

    obtained_ylabel = obtained_plot.get_ylabel()
    expected_ylabel = "Dispatched"
    assert obtained_ylabel == expected_ylabel


def remove_file_if_exists(output_path):
    if os.path.exists(output_path):
        os.remove(output_path)


def test_calculate_x_intercept():
    data = pd.DataFrame({"CPUE": [2, 1], "Cumulative_captures": [1, 2]})
    obtained = dt.calculate_x_intercept(data)
    expected = 3
    assert obtained == expected


raw_data = pd.DataFrame({"CPUE": [19.5, 19, 18.5, 18, 17.5, 17], "Capturas": [1, 2, 3, 4, 5, 6]})


def test_resample_eradication_data():
    rng = np.random.default_rng(42)
    sample = dt.resample_eradication_data(raw_data, rng)
    expected_columns_names = ["CPUE", "Cumulative_captures"]
    assert (sample.columns == expected_columns_names).all()
    assert len(sample) == len(raw_data)


def tests_get_intercepts_distribution():
    bootstrap_number = 10
    obtained = dt.get_intercepts_distribution(raw_data, bootstrap_number)
    obtained_rows = len(obtained)
    assert obtained_rows == bootstrap_number


def test_fit_ramsey_plot():
    data = pd.DataFrame(
        {"CPUE": [19.5, 19, 18.5, 18, 17.5, 17], "Cumulative_captures": [1, 2, 3, 4, 5, 6]}
    )
    obtained_parameters = dt.fit_ramsey_plot(data)
    expected_parameters = np.array([-0.5, 20.0])
    np.testing.assert_array_almost_equal(obtained_parameters, expected_parameters)

    data_error = pd.DataFrame(
        {"CPUE": [19.5, 19, 18.5, 18, 17.5, 17], "Cumulative_captures": [1, 1, 1, 1, 1, 1]}
    )
    with pytest.raises(AssertionError, match=r"^It can not fit Ramsey plot$"):
        dt.fit_ramsey_plot(data_error)

    data_without_error = pd.DataFrame(
        {"CPUE": [19.5, 19, 18.5, 18, 17.5, 17], "Cumulative_captures": [1, 1, 1, 1, 1, 2]}
    )
    assert isinstance(dt.fit_ramsey_plot(data_without_error), type(np.array(0)))


def test_rename_goat_data():
    SPECIES_CONFIG = {"Acumulado": "Cumulative_captures"}
    data = pd.DataFrame({"Acumulado": [1, 2], "CPUE": [2, 3]})
    renamed = dt.set_cumulative_captures_column(data, SPECIES_CONFIG)
    assert all(["Cumulative_captures", "CPUE"] == renamed.columns)

    data = pd.DataFrame({"Cumulative_captures": [1, 2], "CPUE": [2, 3]})
    renamed = dt.set_cumulative_captures_column(data, SPECIES_CONFIG)
    assert all(["Cumulative_captures", "CPUE"] == renamed.columns)
