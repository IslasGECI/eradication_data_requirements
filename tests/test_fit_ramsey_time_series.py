import pandas as pd
import numpy as np
import pytest

from eradication_data_requirements import (
    add_probs_to_effort_capture_data,
    add_slopes_to_effort_capture_data,
    calculate_sample_six_months_slope,
    calculate_six_months_slope,
    extract_prob,
    extract_slopes,
    sample_fit_ramsey_plot,
    set_up_ramsey_time_series,
)


data = pd.DataFrame({"Esfuerzo": [1, 2, 3, 4, 5, 6], "Capturas": [1, 1, 1, 1, 1, 1]})


def test_add_probability_to_effort_capture_data():
    obtained = add_probs_to_effort_capture_data(data)
    contains_slope_column = "prob" in obtained.columns
    assert contains_slope_column
    contains_date_column = "Fecha" in obtained.columns
    assert contains_date_column

    effort_and_capture_data = pd.read_csv(
        "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    )
    obtained = add_probs_to_effort_capture_data(effort_and_capture_data)
    obtained_probs = obtained.prob.iloc[6:]
    is_positive = obtained_probs >= 0
    assert is_positive.all()

    obtained_length = obtained.shape[0]
    expected_length = 10
    assert obtained_length == expected_length

    data_with_zero_effort_row = pd.DataFrame(
        {"Esfuerzo": [1, 2, 3, 4, 5, 6, 0, 3, 0], "Capturas": [1, 1, 1, 1, 1, 1, 0, 1, 0]}
    )
    obtained = add_probs_to_effort_capture_data(data_with_zero_effort_row)


time_series_for_ramsey = pd.DataFrame(
    {"CPUE": [1, 1 / 2, 1 / 3, 1 / 4, 1 / 5, 1 / 6], "Cumulative_captures": [1, 2, 3, 4, 5, 6]}
)


def test_sample_fit_ramsey_plot():
    obtained = sample_fit_ramsey_plot(time_series_for_ramsey)
    expected_length = 6
    obtained_length = len(obtained)
    assert obtained_length == expected_length


def test_extract_prob():
    fitted_parameters = [
        [
            np.array([-0.5, 20.0]),
            np.array([0.5, 20.0]),
            np.array([0.5, 20.0]),
            np.array([0.5, 20.0]),
            np.array([0.5, 20.0]),
            np.array([0.5, 20.0]),
        ]
    ]
    expected = [1 / 6]
    obtained = extract_prob(fitted_parameters)
    assert obtained == expected
    multi_month = [fitted_parameters[0], fitted_parameters[0]]
    expected = [1 / 6, 1 / 6]
    obtained = extract_prob(multi_month)
    assert obtained == expected


def test_add_slopes_to_effort_capture_data():
    obtained = add_slopes_to_effort_capture_data(data)
    contains_slope_column = "slope" in obtained.columns
    assert contains_slope_column
    obtained_no_nan = obtained.slope.count()
    expected_no_nan = 1
    assert obtained_no_nan == expected_no_nan

    effort_and_capture_data = pd.read_csv(
        "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    )
    obtained = add_slopes_to_effort_capture_data(effort_and_capture_data)
    obtained_first_slope = obtained.slope.iloc[5]
    expected_first_slope = 0.0000047
    assert obtained_first_slope == pytest.approx(expected_first_slope, abs=1e-6)


def test_get_status_slopes():
    obtained = add_slopes_to_effort_capture_data(data)
    print(obtained)
    obtained_len = len(obtained)
    expected_len = 6
    assert obtained_len == expected_len


def test_set_up_ramsey_time_series():
    expected = pd.DataFrame(
        {"CPUE": [1, 1 / 2, 1 / 3, 1 / 4, 1 / 5, 1 / 6], "Cumulative_captures": [1, 2, 3, 4, 5, 6]}
    )
    obtained = set_up_ramsey_time_series(data)
    assert (obtained.columns == ["CPUE", "Cumulative_captures"]).all()
    assert (obtained.Cumulative_captures == expected.Cumulative_captures).all()
    assert (obtained.CPUE == expected.CPUE).all()

    data_2 = pd.DataFrame({"Esfuerzo": [2, 2, 2, 2, 2, 2], "Capturas": [1, 2, 1, 1, 2, 1]})
    obtained = set_up_ramsey_time_series(data_2)

    expected = pd.DataFrame(
        {
            "CPUE": [1 / 2, 2 / 2, 1 / 2, 1 / 2, 2 / 2, 1 / 2],
            "Cumulative_captures": [1, 3, 4, 5, 7, 8],
        }
    )
    assert (obtained.Cumulative_captures == expected.Cumulative_captures).all()
    singular_data = pd.DataFrame({"Esfuerzo": [2, 2, 2, 2, 2, 2], "Capturas": [1, 0, 0, 0, 2, 1]})
    obtained = set_up_ramsey_time_series(singular_data)

    expected = pd.DataFrame(
        {
            "CPUE": [1 / 2, 0, 2 / 2, 1 / 2],
            "Cumulative_captures": [1, 1, 3, 4],
        }
    )

    pd.testing.assert_series_equal(
        obtained.Cumulative_captures.reset_index(drop=True),
        expected.Cumulative_captures.reset_index(drop=True),
    )


ramsey_time_series = pd.DataFrame(
    {
        "CPUE": [
            1,
            1 / 2,
            1 / 3,
            1 / 4,
            1 / 5,
            1 / 6,
            1 / 2,
            2 / 2,
            1 / 2,
            1 / 2,
            2 / 2,
            1 / 2,
        ],
        "Cumulative_captures": [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14],
    }
)


def test_calculate_six_months_slope():
    obtained_slopes = calculate_six_months_slope(ramsey_time_series)
    expected_number_slopes = 7
    obtained_number_slopes = len(obtained_slopes)
    assert obtained_number_slopes == expected_number_slopes


def test_calculate_sample_six_months_slope():
    obtained_slopes = calculate_sample_six_months_slope(time_series_for_ramsey)
    expected_number_slopes = 1
    obtained_number_slopes = len(obtained_slopes)
    assert obtained_number_slopes == expected_number_slopes
    expected_number_elements = 6
    obtained_number_elements = len(obtained_slopes[0])
    assert obtained_number_elements == expected_number_elements
    print(obtained_slopes)


def test_extract_slopes():
    slopes_and_intercept = [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]
    expected_slopes = [1, 3, 5]
    obtained_slopes = extract_slopes(slopes_and_intercept)
    assert obtained_slopes == expected_slopes
