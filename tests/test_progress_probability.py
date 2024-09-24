import pandas as pd
import pytest
import numpy as np


from eradication_data_requirements.progress_probability import (
    calculate_progress_probability,
    get_progress_probability,
    get_slope,
    get_slopes_distribution,
)

raw_data_2 = pd.DataFrame({"CPUE": [1, 1, 18.5, 18, 17.5, 27], "Capturas": [1, 2, 3, 4, 5, 6]})
bootstrap_number = 10
seed = 42


def tests_get_progress_probability():
    bootstrap_number = 60
    obtained = get_progress_probability(raw_data_2, bootstrap_number, seed)
    assert isinstance(obtained, float)
    positions_after_decimal = str(obtained)[::-1].find(".")
    assert positions_after_decimal <= 3


def tests_calculate_progress_probability():
    slopes = [1, 0.5, 0, -0.5, -1]
    obtained = calculate_progress_probability(slopes)
    expected = 2 / 5
    assert obtained == expected

    slopes = [1, 0.5, 0, -0.5, -1, np.nan, -0.7]
    obtained = calculate_progress_probability(slopes)
    expected = 3 / 6
    assert obtained == expected


def tests_get_slopes_distribution():
    obtained = get_slopes_distribution(raw_data_2, bootstrap_number, seed)
    obtained_rows = len(obtained)
    assert obtained_rows == bootstrap_number

    assert isinstance(obtained[0], float)
    assert pytest.approx(obtained[0], abs=1e-3) == 0.83

    raw_data_low_captures = pd.DataFrame(
        {"CPUE": [1, 0, 0, 0, 0, 27], "Capturas": [1, 0, 0, 0, 0, 1]}
    )
    obtained = get_slopes_distribution(raw_data_low_captures, bootstrap_number, seed)
    obtained_rows = len(obtained)
    assert obtained_rows == bootstrap_number


def test_get_slope():
    data = pd.DataFrame({"CPUE": [2, 1], "Cumulative_captures": [1, 2]})
    obtained = get_slope(data)
    expected_slope = -1
    assert pytest.approx(obtained) == expected_slope
