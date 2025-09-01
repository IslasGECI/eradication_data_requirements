from eradication_data_requirements.adapters import adapt_effort_and_catpures
import pandas as pd


def test_adapt_effort_and_captures():
    data = pd.read_csv("tests/data/esfuerzo_capturas_gatos_guadalupe_ISO_for_tests.csv")
    obtained = adapt_effort_and_catpures(data)
    expected_colummn = "Season"
    assert expected_colummn in obtained.columns
