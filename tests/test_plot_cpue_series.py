from eradication_data_requirements.plot_cpue_series import plot_cumulative_series_cpue
import geci_test_tools as gtt

import pandas as pd


def tests_plot_cumulative_series_cpue():
    effort_capture_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    effort_capture_df = pd.read_csv(effort_capture_path)
    output_png = "tests/figures/annual_cpue_time_series.png"
    font_size = 27
    plot_cumulative_series_cpue(effort_capture_df, output_png, font_size)
    expected_hash = "1026fc4e26d645bbeba7fdae0245e52e"
    obtained_hash = gtt.calculate_hash(output_png)
    assert obtained_hash == expected_hash
