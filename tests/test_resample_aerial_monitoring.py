import pandas as pd

from eradication_data_requirements import get_sum_distribution, get_monitoring_dict


def test_get_monitoring_dict():
    raw_data = pd.read_csv("tests/data/monitoreo_cabras_magdalena.csv")
    bootstrap_number = 10
    obtained = get_monitoring_dict(raw_data, bootstrap_number)
    assert isinstance(obtained, dict)


def test_get_sum_distribution():
    goats_data = pd.DataFrame({"No_goats": [1, 3, 5, 7, 9, 12, 14, 50, 50]})
    bootstrap_number = 10
    obtained = get_sum_distribution(goats_data, bootstrap_number)
    assert len(obtained) == bootstrap_number
    assert isinstance(obtained[0], int)
