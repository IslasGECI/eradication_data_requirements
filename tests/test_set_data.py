import pandas as pd

from eradication_data_requirements import filter_data_by_method


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
