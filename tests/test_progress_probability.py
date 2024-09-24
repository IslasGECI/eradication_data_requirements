import pandas as pd
import pytest

from eradication_data_requirements.progress_probability import get_slope, get_slopes_distribution


def tests_get_slopes_distribution():
    raw_data_2 = pd.DataFrame({"CPUE": [1, 1, 18.5, 18, 17.5, 27], "Capturas": [1, 2, 3, 4, 5, 6]})
    bootstrap_number = 10
    seed = 42
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
