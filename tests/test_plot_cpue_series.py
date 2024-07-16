from eradication_data_requirements.plot_cpue_series import (
    plot_cumulative_series_cpue_by_season,
    plot_cumulative_series_cpue,
)
import geci_test_tools as gtt

import pandas as pd
import matplotlib as mpl
import pytest


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


def tests_plot_cumulative_series_cpue_by_season():
    effort_capture_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    effort_capture_df = pd.read_csv(effort_capture_path)
    font_size = 27
    output_png = "tests/data/annual_cpue_time_series.png"
    gtt.if_exist_remove(output_png)
    plot_cumulative_series_cpue_by_season(effort_capture_df, output_png, font_size)
    expected_hash = "377cd484da57f7bacda783aeb1d199e2"
    obtained_hash = gtt.calculate_hash(output_png)
    assert obtained_hash == expected_hash
