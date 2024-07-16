from eradication_data_requirements.plot_cpue_series import (
    calculate_cpue_and_cumulative_by_flight,
    plot_cumulative_series_cpue,
)

import pandas as pd
import matplotlib as mpl
import pytest


def tests_calculate_cpue_and_cumulative_by_flight():
    effort_goats_raw = pd.read_csv("tests/data/feral_goat_capture_effort.csv")
    obtained = calculate_cpue_and_cumulative_by_flight(effort_goats_raw)
    obtained_number_columns = len(obtained.columns)
    expected_number_columns = len(effort_goats_raw) + 2
    assert obtained_number_columns == expected_number_columns


def test_plot_cumulative_series_cpue():
    cpue_data_path = "tests/data/processed_yearly_cpue_for_plot.csv"
    cpue_df = pd.read_csv(cpue_data_path)
    fontsize = 20
    obtained = plot_cumulative_series_cpue(fontsize, cpue_df)
    assert isinstance(obtained[0], mpl.axes._axes.Axes)
    obtained_cpue_ylim = obtained[0].get_ylim()
    obtained_cum_cpue_ylim = obtained[1].get_ylim()
    assert pytest.approx(obtained_cpue_ylim, abs=1e-4) == (0, 0.0006)
    assert pytest.approx(obtained_cum_cpue_ylim, abs=1e-4) == (0, 0.0008)
