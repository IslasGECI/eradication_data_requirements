from eradication_data_requirements import resample_valid_data, validate_samples_to_fit

import pandas as pd

effort_and_capture_data = pd.read_csv("tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv")


def test_resample_valid_data():
    seed = 42
    obtained = resample_valid_data(effort_and_capture_data[0:5], seed)
    expected_len = 6
    obtained_len = len(obtained)
    assert obtained_len == expected_len

    seed = 3
    obtained = resample_valid_data(effort_and_capture_data[4:9], seed)
    expected_len = 0
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
