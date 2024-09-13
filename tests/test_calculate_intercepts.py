import pandas as pd
import numpy as np

import eradication_data_requirements as edr

raw_data = pd.DataFrame({"CPUE": [19.5, 19, 18.5, 18, 17.5, 17], "Capturas": [1, 2, 3, 4, 5, 6]})

seed = 42


def tests_get_population_status_dict():
    bootstrap_number = 20
    obtained = edr.get_population_status_dict(raw_data, bootstrap_number, seed)
    assert isinstance(obtained, dict)
    expected_n0_interval = "188 (127 - 317)"
    assert obtained["n0"] == expected_n0_interval

    expected_remanents = "167 (106 - 296)"
    assert obtained["remanentes"] == expected_remanents


def tests_remaining_interval():
    n0_interval = [10, 100, 120]
    capturas = 20
    obtained = edr.remaining_interval(n0_interval, capturas)
    assert obtained[0] == 0


def test_resample_eradication_data():
    rng = np.random.default_rng(seed)
    sample = edr.resample_eradication_data(raw_data, rng)
    print(sample)
    expected_columns_names = ["CPUE", "Cumulative_captures"]
    assert (sample.columns == expected_columns_names).all()
    assert len(sample) == len(raw_data)

    assert (sample.Cumulative_captures.diff()[1:] > 0).all()
    assert (sample.index.diff()[1:] >= 0).all()


def tests_get_intercepts_distribution():
    raw_data = pd.DataFrame({"CPUE": [1, 1, 18.5, 18, 17.5, 27], "Capturas": [1, 2, 3, 4, 5, 6]})
    bootstrap_number = 10
    obtained = edr.get_intercepts_distribution(raw_data, bootstrap_number)
    obtained_rows = len(obtained)
    assert obtained_rows == bootstrap_number
    assert (np.array(obtained) > 0).all()


def test_calculate_x_intercept():
    data = pd.DataFrame({"CPUE": [2, 1], "Cumulative_captures": [1, 2]})
    obtained = edr.calculate_x_intercept(data)
    expected = 3
    assert obtained == expected
