import pandas as pd
import numpy as np
import pytest

from eradication_data_requirements import (
    add_empty_column,
    add_probs_to_effort_capture_data,
    add_slopes_to_effort_capture_data,
    calculate_resampled_slope_by_window,
    calculate_six_months_slope,
    extract_prob,
    extract_slopes,
    fit_resampled_cumulative,
    paste_status,
    fit_resampled_captures,
    set_up_ramsey_time_series,
)


data = pd.DataFrame(
    {
        "Esfuerzo": [1, 2, 3, 4, 5, 6],
        "Capturas": [1, 1, 1, 1, 1, 1],
        "Fecha": [2018, 2019, 2020, 2021, 2022, 2023],
    }
)


def test_add_probability_to_effort_capture_data():
    bootstrapping_number = 10
    window_length = 6
    obtained = add_probs_to_effort_capture_data(data, bootstrapping_number, window_length)
    contains_slope_column = "prob" in obtained.columns
    assert contains_slope_column
    contains_date_column = "Fecha" in obtained.columns
    assert contains_date_column
    assert obtained.Fecha[0] == data.Fecha[0]

    effort_and_capture_data = pd.read_csv(
        "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    )
    obtained = add_probs_to_effort_capture_data(
        effort_and_capture_data, bootstrapping_number, window_length
    )
    obtained_probs = obtained.prob.iloc[6:]
    is_positive = obtained_probs >= 0
    assert is_positive.all()

    obtained_length = obtained.shape[0]
    expected_length = 13
    assert obtained_length == expected_length

    data_with_zero_effort_row = pd.DataFrame(
        {
            "Esfuerzo": [1, 2, 3, 4, 5, 6, 0, 3, 0],
            "Capturas": [1, 1, 1, 1, 1, 1, 0, 1, 0],
            "Fecha": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        }
    )
    obtained = add_probs_to_effort_capture_data(
        data_with_zero_effort_row, bootstrapping_number, window_length
    )
    assert obtained.shape[0] == (len(data_with_zero_effort_row) - 2)


time_series_for_ramsey = pd.DataFrame(
    {"CPUE": [1, 1 / 2, 1 / 3, 1 / 4, 1 / 5, 1 / 6], "Cumulative_captures": [1, 2, 3, 4, 5, 6]}
)


def test_fit_resampled_cumulative():
    bootstrapping_number = 10
    obtained = fit_resampled_cumulative(data, bootstrapping_number)
    obtained_list_len = len(obtained)
    assert obtained_list_len == bootstrapping_number
    assert obtained[0].shape == (2,)


def test_resampled_fit_ramsey_plot():
    bootstrapping_number = 10
    obtained = fit_resampled_captures(data, bootstrapping_number)
    obtained_list_len = len(obtained)
    assert obtained_list_len == bootstrapping_number

    assert obtained[0].shape == (2,)


def test_extract_prob():
    fitted_parameters = [
        [
            np.array([-0.5, 20.0]),
            np.array([0.5, 20.0]),
            np.array([0.5, 20.0]),
            np.array([0.5, 20.0]),
            np.array([0.5, 20.0]),
            np.array([0, 20.0]),
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
        {
            "CPUE": [1, 1 / 2, 1 / 3, 1 / 4, 1 / 5, 1 / 6],
            "Cumulative_captures": [1, 2, 3, 4, 5, 6],
            "Fecha": [2018, 2019, 2020, 2021, 2022, 2023],
        }
    )
    obtained = set_up_ramsey_time_series(data)
    assert (obtained.columns == ["Fecha", "CPUE", "Cumulative_captures"]).all()
    assert (obtained.Cumulative_captures == expected.Cumulative_captures).all()
    assert (obtained.CPUE == expected.CPUE).all()
    assert (obtained.Fecha == expected.Fecha).all()

    data_2 = pd.DataFrame(
        {
            "Esfuerzo": [2, 2, 2, 2, 2, 2],
            "Capturas": [1, 2, 1, 1, 2, 1],
            "Fecha": [2018, 2019, 2020, 2021, 2022, 2023],
        }
    )
    obtained = set_up_ramsey_time_series(data_2)

    expected = pd.DataFrame(
        {
            "CPUE": [1 / 2, 2 / 2, 1 / 2, 1 / 2, 2 / 2, 1 / 2],
            "Cumulative_captures": [1, 3, 4, 5, 7, 8],
        }
    )
    assert (obtained.Cumulative_captures == expected.Cumulative_captures).all()
    singular_data = pd.DataFrame(
        {
            "Esfuerzo": [2, 2, 2, 2, 2, 2],
            "Capturas": [1, 0, 0, 0, 2, 1],
            "Fecha": [2018, 2019, 2020, 2021, 2022, 2023],
        }
    )
    obtained = set_up_ramsey_time_series(singular_data)

    expected = pd.DataFrame(
        {
            "CPUE": [1 / 2, 0, 0, 0, 2 / 2, 1 / 2],
            "Cumulative_captures": [1, 1, 1, 1, 3, 4],
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
    bootstrapping_number = 10
    window_length = 6
    obtained_slopes = calculate_resampled_slope_by_window(data, bootstrapping_number, window_length)
    expected_number_slopes = 1
    obtained_number_slopes = len(obtained_slopes)
    assert obtained_number_slopes == expected_number_slopes

    obtained_number_elements = len(obtained_slopes[0])
    assert obtained_number_elements == bootstrapping_number
    np.testing.assert_array_almost_equal(obtained_slopes[0][1][0], -0.12095238)
    np.testing.assert_array_almost_equal(obtained_slopes[0][4][0], -0.05)


def test_extract_slopes():
    slopes_and_intercept = [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]
    expected_slopes = [1, 3, 5]
    obtained_slopes = extract_slopes(slopes_and_intercept)
    assert obtained_slopes == expected_slopes


def test_paste_status():
    length_one_dataframe = pd.DataFrame({"slope": [1 / 2]})
    with pytest.raises(AssertionError, match=r"^Different dimensions$"):
        paste_status(ramsey_time_series, length_one_dataframe, column_name="slope")


def test_add_empty_column():
    ramsey_time_series_copy = ramsey_time_series.copy()
    column_name = "slope"
    ramsey_time_series_copy = add_empty_column(ramsey_time_series_copy, column_name)
    assert isinstance(ramsey_time_series_copy[column_name][0], type(np.nan))
