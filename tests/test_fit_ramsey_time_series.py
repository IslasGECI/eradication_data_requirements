import pandas as pd
import numpy as np
import pytest

from eradication_data_requirements.fit_ramsey_time_series import (
    add_empty_column,
    add_probs_to_effort_capture_data,
    calculate_resampled_probability_by_window,
    calculate_six_months_slope,
    complete_missing_months_in_year,
    extract_prob,
    extract_slopes,
    fit_resampled_cumulative,
    paste_status,
    fit_resampled_captures,
    fill_missing_months_with_effort_one_and_captures_zero,
    set_up_ramsey_time_series,
)


data = pd.DataFrame(
    {
        "Esfuerzo": [1, 2, 3, 4, 5, 6],
        "CPUE": [1, 2, 3, 4, 5, 6],
        "Capturas": [1, 1, 1, 1, 1, 1],
        "Fecha": [2018, 2019, 2020, 2021, 2022, 2023],
    }
)


def test_add_probability_to_effort_capture_data():

    data_ = pd.DataFrame(
        {
            "Esfuerzo": [1, 2, 3, 4, 5, 6],
            "Capturas": [1, 1, 1, 1, 1, 1],
            "Fecha": [
                "2018-01-01",
                "2018-04-01",
                "2018-08-01",
                "2018-09-01",
                "2018-10-01",
                "2019-01-01",
            ],
        }
    )

    bootstrapping_number = 10
    window_length = 6
    obtained = add_probs_to_effort_capture_data(data_, bootstrapping_number, window_length)
    contains_slope_column = "prob" in obtained.columns
    assert contains_slope_column
    contains_date_column = "Fecha" in obtained.columns
    assert contains_date_column
    assert obtained.Fecha[0] == data_.Fecha[0]

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
            "Fecha": [
                "2015-01-01",
                "2015-02-01",
                "2015-03-01",
                "2015-08-01",
                "2015-09-01",
                "2015-11-01",
                "2015-12-01",
                "2016-01-01",
                "2016-04-01",
            ],
        }
    )
    obtained = add_probs_to_effort_capture_data(
        data_with_zero_effort_row, bootstrapping_number, window_length
    )
    are_all_efforts_not_zero = (obtained.Esfuerzo != 0).all()
    assert are_all_efforts_not_zero


def test_complete_missing_months_in_year():
    incomplete_months = pd.DataFrame(
        {
            "Fecha": ["2015-04-01", "2015-06-01", "2015-12-01"],
        }
    )
    obtained = complete_missing_months_in_year(incomplete_months)
    expected_len = 12
    assert obtained.shape[0] == expected_len

    incomplete_months_with_january = pd.DataFrame(
        {
            "Fecha": ["2015-01-01", "2015-06-01", "2015-12-01"],
        }
    )
    obtained = complete_missing_months_in_year(incomplete_months_with_january)
    expected_len = 12
    assert obtained.shape[0] == expected_len


def test_fill_missing_months_with_effort_one_and_captures_zero():

    incomplete_months = pd.DataFrame(
        {
            "Esfuerzo": [1, 2, 3],
            "Capturas": [1, 1, 1],
            "Fecha": ["2015-01-01", "2015-10-01", "2015-12-01"],
        }
    )
    obtained = fill_missing_months_with_effort_one_and_captures_zero(incomplete_months)
    expected_len = 12
    assert obtained.shape[0] == expected_len

    incomplete_months_2 = pd.DataFrame(
        {
            "Esfuerzo": [1, 2, 3],
            "Capturas": [1, 1, 1],
            "Fecha": ["2015-04-01", "2015-10-01", "2015-12-01"],
        }
    )
    obtained = fill_missing_months_with_effort_one_and_captures_zero(incomplete_months_2)
    expected_len = 12
    assert obtained.shape[0] == expected_len


time_series_for_ramsey = pd.DataFrame(
    {"CPUE": [1, 1 / 2, 1 / 3, 1 / 4, 1 / 5, 1 / 6], "Cumulative_captures": [1, 2, 3, 4, 5, 6]}
)


def test_fit_resampled_cumulative():
    bootstrapping_number = 10
    obtained = fit_resampled_cumulative(data, bootstrapping_number)
    obtained_list_len = len(obtained)
    assert obtained_list_len == bootstrapping_number
    assert obtained[0].shape == (2,)

    data_failing = pd.DataFrame(
        {
            "Esfuerzo": [1, 2, 3, 4, 5, 6],
            "Capturas": [1, 0, 0, 0, 0, 0],
            "Fecha": [2018, 2019, 2020, 2021, 2022, 2023],
        }
    )

    obtained = fit_resampled_cumulative(data_failing, bootstrapping_number)
    obtained_list_len = len(obtained)
    assert obtained_list_len == 0


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


def test_calculate_resampled_probability_by_window():
    bootstrapping_number = 10
    window_length = 6
    obtained_probability_by_window = calculate_resampled_probability_by_window(
        data, bootstrapping_number, window_length
    )
    expected_probability_by_window = 1
    obtained_number_of_probabilities = len(obtained_probability_by_window)
    assert obtained_number_of_probabilities == expected_probability_by_window

    data_for_two_probabilities = pd.DataFrame(
        {
            "Esfuerzo": [1, 2, 3, 4, 5, 6, 7],
            "CPUE": [1, 2, 3, 4, 5, 6, 7],
            "Capturas": [1, 1, 1, 1, 1, 1, 1],
            "Fecha": [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        }
    )
    obtained_probability_by_window = calculate_resampled_probability_by_window(
        data_for_two_probabilities, bootstrapping_number, window_length
    )
    expected_probability_by_window = 2
    obtained_number_of_probabilities = len(obtained_probability_by_window)
    assert obtained_number_of_probabilities == expected_probability_by_window


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
