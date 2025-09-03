from eradication_data_requirements.plot_cpue_series import (
    calculate_cpue_and_cumulative_by_flight,
    plot_comparative_yearly_cpue,
    plot_cumulative_series_cpue,
    plot_yearly_cpue,
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


def test_plot_yearly_cpue():
    cpue_data_path = "tests/data/processed_yearly_cpue_for_plot.csv"
    cpue_df = pd.read_csv(cpue_data_path)
    fontsize = 20
    obtained_ax = plot_yearly_cpue(fontsize, cpue_df)
    assert isinstance(obtained_ax, mpl.axes._axes.Axes)
    obtained_cpue_ylim = obtained_ax.get_ylim()
    assert pytest.approx(obtained_cpue_ylim, abs=1e-4) == (0, 0.0006)
    obtained_cpue_ylabel = obtained_ax.get_ylabel()
    assert obtained_cpue_ylabel == "Catch Per Unit Effort (CPUE)"
    mpl.pyplot.savefig("yearly_cpue.png")


def test_plot_comparative_yearly_cpue():
    cpue_yearly_data_path = "tests/data/processed_yearly_cpue_for_plot.csv"
    cpue_yearly_socorro = pd.read_csv(cpue_yearly_data_path)
    cpue_yearly_guadalupe = cpue_yearly_socorro
    obtained_ax = plot_comparative_yearly_cpue(cpue_yearly_socorro, cpue_yearly_guadalupe)
    assert isinstance(obtained_ax, mpl.axes._axes.Axes)

    expected_lines = 2
    assert len(obtained_ax.get_lines()) == expected_lines

    mpl.pyplot.savefig("salida.png")
    assert obtained_ax.get_legend().get_texts()[0].get_text() == "Socorro"
    assert obtained_ax.get_legend().get_texts()[1].get_text() == "Guadalupe"
