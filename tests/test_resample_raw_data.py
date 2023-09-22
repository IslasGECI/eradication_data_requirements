from eradication_data_requirements import (
    resample_valid_data,
    validate_samples_to_fit,
    validate_cumulative_samples_to_fit,
)

import pandas as pd

effort_and_capture_data = pd.read_csv("tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv")


def test_resample_valid_data():
    bootstrapping_number = 5
    obtained = resample_valid_data(effort_and_capture_data[0:5], bootstrapping_number)
    obtained_len = len(obtained)
    assert obtained_len == bootstrapping_number

    expected_len_dataframe = 6
    obtained_len_dataframe = obtained[0].shape[0]
    assert obtained_len_dataframe == expected_len_dataframe

    bootstrapping_number = 4
    obtained = resample_valid_data(effort_and_capture_data[4:9], bootstrapping_number)
    expected_len = 3
    obtained_len = len(obtained)
    assert obtained_len == expected_len


def test_resample_valid_cumulative_data():
    cumulative_data = pd.DataFrame(
        {"Cumulative_captures": [14, 14, 14, 14, 14, 14, 14, 15, 15, 23, 23, 26]}
    )
    bootstrapping_number = 4
    obtained = resample_valid_cumulative_data(cumulative_data[0:6], bootstrapping_number)
    expected_len = 0
    obtained_len = len(obtained)
    assert obtained_len == expected_len


def tests_validate_cumulative_samples_to_fit():
    valid_data = pd.DataFrame({"Cumulative_captures": [14, 15, 15, 23, 23, 26]})
    non_valid_data = pd.DataFrame({"Cumulative_captures": [14, 14, 14, 14, 14, 14]})
    samples = [valid_data, non_valid_data]
    obtained = validate_cumulative_samples_to_fit(samples)
    expected_len = 1
    obtained_len = len(obtained)
    assert obtained_len == expected_len


def test_validate_samples_to_fit():
    non_valid_data = pd.DataFrame({"Capturas": [14, 0, 0, 0, 0, 0]})
    valid_data = pd.DataFrame({"Capturas": [14, 1, 0, 8, 0, 3]})
    non_valid_data_zeros = pd.DataFrame({"Capturas": [0, 0, 0, 0, 0, 0]})
    sampled_data = [non_valid_data, valid_data, non_valid_data_zeros]
    obtained = validate_samples_to_fit(sampled_data)
    expected_len = 1
    obtained_len = len(obtained)
    assert obtained_len == expected_len
