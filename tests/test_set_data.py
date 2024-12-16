import pandas as pd

from eradication_data_requirements.set_data import (
    filter_data_by_method,
    select_december_of_every_year,
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


def test_select_dec_of_every_year():
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
    obtained = select_december_of_every_year(data)
    expected_number_of_rows = 3
    obtained_number_of_rows = len(obtained)
    assert obtained_number_of_rows == expected_number_of_rows
