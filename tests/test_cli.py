from eradication_data_requirements import (
    write_effort_and_captures_with_probability,
    write_effort_and_captures_with_slopes,
)

import numpy as np
import pandas as pd
import os

input_path = "tests/data/esfuerzo_capturas_semanales_iso8601.csv"


def test_write_effort_and_capture_with_probability():
    output_path = "tests/data/probability_time_series.csv"
    monthly_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    if os.path.exists(output_path):
        os.remove(output_path)
    write_effort_and_captures_with_probability(monthly_path, output_path)
    assert os.path.exists(output_path)
    obtained = pd.read_csv(output_path)

    obtained_probability = obtained.prob
    expected_probability = pd.Series(
        [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            1 / 6,
            1.0,
            1.0,
            5 / 6,
            1 / 2,
        ],
        name="prob",
    )
    pd.testing.assert_series_equal(obtained_probability, expected_probability)


def test_write_effort_and_capture_with_slopes():
    output_path = "tests/data/slope_time_series.csv"
    monthly_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    if os.path.exists(output_path):
        os.remove(output_path)
    write_effort_and_captures_with_slopes(monthly_path, output_path)
    assert os.path.exists(output_path)
    obtained = pd.read_csv(output_path)

    obtained_slopes = obtained.slope
    expected_slopes = pd.Series(
        [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            4.739e-6,
            -1.117e-5,
            -9.646e-6,
            -5.082e-5,
            -2.781e-6,
        ],
        name="slope",
    )
    print(obtained_slopes)
    pd.testing.assert_series_equal(obtained_slopes, expected_slopes)
