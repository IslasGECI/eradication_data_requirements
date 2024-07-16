from eradication_data_requirements.plot_cpue_series import (
    plot_cumulative_series_cpue_by_season,
    plot_cumulative_series_cpue,
    calculate_cpue_and_cumulative_by_season,
)
import geci_test_tools as gtt

import pandas as pd
import matplotlib as mpl


cpue_data_path = "tests/data/processed_yearly_cpue_for_plot.csv"
output_png = "tests/data/annual_cpue_time_series.png"


def test_plot_cumulative_series_cpue():
    cpue_df = pd.read_csv(cpue_data_path)
    fontsize = 20
    obtained = plot_cumulative_series_cpue(output_png, fontsize, cpue_df)
    assert isinstance(obtained, mpl.axes._axes.Axes)


def tests_plot_cumulative_series_cpue_by_season():
    effort_capture_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    effort_capture_df = pd.read_csv(effort_capture_path)
    font_size = 27
    gtt.if_exist_remove(output_png)
    plot_cumulative_series_cpue_by_season(effort_capture_df, output_png, font_size)
    expected_hash = "1026fc4e26d645bbeba7fdae0245e52e"
    obtained_hash = gtt.calculate_hash(output_png)
    assert obtained_hash == expected_hash
