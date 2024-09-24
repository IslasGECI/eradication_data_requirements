import pandas as pd
import pytest

from eradication_data_requirements.progress_probability import get_slope, get_slopes_distribution


def tests_get_slopes_distribution():
    raw_data_2 = pd.DataFrame({"CPUE": [1, 1, 18.5, 18, 17.5, 27], "Capturas": [1, 2, 3, 4, 5, 6]})
    bootstrap_number = 10
    obtained = get_slopes_distribution(raw_data_2, bootstrap_number)
    obtained_rows = len(obtained)
    assert obtained_rows == bootstrap_number


def test_get_slope():
    data = pd.DataFrame({"CPUE": [2, 1], "Cumulative_captures": [1, 2]})
    obtained = get_slope(data)
    expected_slope = -1
    assert pytest.approx(obtained) == expected_slope
