import pandas as pd
import pytest

from eradication_data_requirements.progress_probability import get_slope


def test_get_slope():
    data = pd.DataFrame({"CPUE": [2, 1], "Cumulative_captures": [1, 2]})
    obtained = get_slope(data)
    expected_slope = -1
    assert pytest.approx(obtained) == expected_slope
