import pandas as pd
import json

from bootstrapping_tools import Bootstrap_from_time_series_parametrizer
from eradication_data_requirements import ProgressBootstrapper

raw_data = pd.DataFrame(
    {
        "Esfuerzo": [1 / 19.5, 2 / 19, 3 / 18.5, 4 / 18, 5 / 17.5, 6 / 17],
        "Capturas": [1, 2, 3, 4, 5, 6],
    }
)


def test_ProgressBootstrapper():
    independent_variable = "Capturas"
    bootstrap_number = 100
    parametrizer = Bootstrap_from_time_series_parametrizer(
        blocks_length=1,
        column_name="CPUE",
        N=bootstrap_number,
        independent_variable=independent_variable,
    )
    parametrizer.set_data(raw_data)
    bootstrapper = ProgressBootstrapper(parametrizer)

    obtained_cpue = bootstrapper.add_cpue()
    assert "CPUE" in obtained_cpue.columns
    expected_cpue = [19.5, 19, 18.5, 18, 17.5, 17]
    assert (obtained_cpue.CPUE == expected_cpue).all()

    obtained = bootstrapper.parameters_distribution
    obtained_rows = len(obtained)
    assert obtained_rows == bootstrap_number

    output_path = "tests/data/progress_intervals.json"
    bootstrapper.save_intervals(output_path)
    with open(output_path) as json_file:
        obtained_json = json.load(json_file)
    obtained_fields = list(obtained_json.keys())
    expected_fields = [
        "intervals",
        "slopes_latex_interval",
        "p-values",
        "bootstrap_intermediate_distribution",
    ]
    assert set(obtained_fields) == set(expected_fields)
