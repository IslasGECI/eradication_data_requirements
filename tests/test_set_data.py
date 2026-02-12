import pandas as pd

from eradication_data_requirements.set_data import (
    filter_data_by_method,
    select_month_by_resolution,
)


def test_filter_data_by_method():
    raw_data = pd.DataFrame(
        {
            "Tecnica": ["Extracción viva (arreo)", "Cacería terrestre", "Cacería terrestre"],
            "Capturas": [10, 20, 30],
        }
    )
    method = "Cacería terrestre"
    obtained = filter_data_by_method(raw_data, method)
    expected_rows = 2
    assert len(obtained) == expected_rows

    assert "Acumulado" in obtained.columns


data = pd.DataFrame(
    {
        "Fecha": [
            "2014-05-01",
            "2014-06-01",
            "2014-09-01",
            "2014-12-01",
            "2015-03-01",
            "2015-05-01",
            "2015-07-01",
            "2015-12-01",
            "2016-01-01",
        ],
        "prob": [0, 1, 2, 3, 4, 5, 6, 7, 8],
    }
)


def tests_select_month_by_window_length():
    data = pd.DataFrame(
        {
            "Fecha": [
                "2014-01-01",
                "2014-02-01",
                "2014-03-01",
                "2014-04-01",
                "2014-05-01",
                "2014-06-01",
                "2014-07-01",
                "2014-08-01",
                "2014-09-01",
                "2014-10-01",
                "2014-11-01",
                "2014-12-01",
                "2015-01-01",
                "2015-02-01",
            ],
            "prob": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        }
    )
    window_length = 12
    obtained = select_month_by_resolution(data.iloc[0:12], window_length)
    expected_number_of_rows = 1
    obtained_number_of_rows = len(obtained)

    assert obtained_number_of_rows == expected_number_of_rows
    obtained = select_month_by_resolution(data, window_length)
    expected_number_of_rows = 2
    obtained_number_of_rows = len(obtained)
    assert obtained_number_of_rows == expected_number_of_rows

    window_length = 6
    obtained = select_month_by_resolution(data, window_length)
    expected_number_of_rows = 3
    obtained_number_of_rows = len(obtained)
    assert obtained_number_of_rows == expected_number_of_rows
    assert all(obtained == [5, 11, 13])
