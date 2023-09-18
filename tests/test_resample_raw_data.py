from eradication_data_requirements import resample_valid_data

import pandas as pd

effort_and_capture_data = pd.read_csv("tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv")


def test_resample_valid_data():
    seed = 42
    obtained = resample_valid_data(effort_and_capture_data[0:5], seed)
    expected_len = 6
    obtained_len = obtained.shape[0]
    assert obtained_len == expected_len
