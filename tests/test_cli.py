from eradication_data_requirements import app
import geci_test_tools as gtt

import numpy as np
import pandas as pd
from typer.testing import CliRunner


input_path = "tests/data/esfuerzo_capturas_semanales_iso8601.csv"
runner = CliRunner()


def tests_plot_cumulative_series_cpue_by_flight():
    result = runner.invoke(app, ["plot-cumulative-series-cpue-by-flight", "--help"])
    assert result.exit_code == 0
    assert " Input file path " in result.stdout
    assert " Output file path " in result.stdout
    assert "[default: 27 " not in result.stdout

    effort_capture_path = "tests/data/feral_goat_capture_effort.csv"
    font_size = 27
    output_png = "tests/data/flight_cpue_time_series.png"
    gtt.if_exist_remove(output_png)

    result = runner.invoke(
        app,
        [
            "plot-cumulative-series-cpue-by-flight",
            "--effort-capture-path",
            effort_capture_path,
            "--output-png",
            output_png,
            "--fontsize",
            font_size,
        ],
    )
    assert result.exit_code == 0
    gtt.assert_exist(output_png)
    gtt.if_exist_remove(output_png)


def tests_plot_cumulative_series_cpue_by_season():
    result = runner.invoke(app, ["plot-cumulative-series-cpue-by-season", "--help"])
    assert result.exit_code == 0
    assert " Input file path " in result.stdout
    assert " Output file path " in result.stdout
    assert "[default: 27 " not in result.stdout

    effort_capture_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    font_size = 27
    output_png = "tests/data/annual_cpue_time_series.png"
    gtt.if_exist_remove(output_png)

    result = runner.invoke(
        app,
        [
            "plot-cumulative-series-cpue-by-season",
            "--effort-capture-path",
            effort_capture_path,
            "--output-png",
            output_png,
            "--fontsize",
            font_size,
        ],
    )
    assert result.exit_code == 0
    gtt.assert_exist(output_png)
    gtt.if_exist_remove(output_png)


def test_write_progress_probability_figure():
    result = runner.invoke(app, ["write-progress-probability-figure", "--help"])
    assert " Input file path " in result.stdout
    assert " Output file path " in result.stdout
    assert "[default: " not in result.stdout

    data_path = "tests/data/progress_probability_tests.csv"
    figure_path = "tests/data/progress_probability_tests.png"

    gtt.if_exist_remove(figure_path)

    result = runner.invoke(
        app,
        [
            "write-progress-probability-figure",
            "--data-path",
            data_path,
            "--figure-path",
            figure_path,
        ],
    )
    assert result.exit_code == 0

    gtt.assert_exist(figure_path)
    gtt.if_exist_remove(figure_path)


monthly_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"


def test_write_effort_and_capture_with_probability():
    output_path = "tests/data/probability_time_series.csv"

    window_length = 6
    result = runner.invoke(app, ["write-effort-and-captures-with-probability", "--help"])
    assert " Input file path " in result.stdout
    assert " Bootstrapping number " in result.stdout
    assert " Output file path " in result.stdout
    assert " Window length for removal rate " in result.stdout
    assert "[default: captures" in result.stdout

    gtt.if_exist_remove(output_path)

    result = runner.invoke(
        app,
        [
            "write-effort-and-captures-with-probability",
            "--input-path",
            monthly_path,
            "--bootstrapping-number",
            100,
            "--output-path",
            output_path,
            "--window-length",
            window_length,
        ],
    )
    assert result.exit_code == 0
    gtt.assert_exist(output_path)
    obtained = pd.read_csv(output_path)
    assert obtained.shape[1] == 4

    obtained_probability = obtained.prob
    expected_probability = pd.Series(
        [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            0.36363636363636365,
            0.4387755102040816,
            0.3118279569892473,
            0.21518987341772153,
            0.15853658536585366,
            0.15476190476190477,
            0.23469387755102042,
            0.3838383838383838,
        ],
        name="prob",
    )
    pd.testing.assert_series_equal(obtained_probability, expected_probability)
    gtt.if_exist_remove(output_path)


def test_write_effort_and_capture_with_slopes():
    output_path = "tests/data/slope_time_series.csv"

    result = runner.invoke(app, ["write-effort-and-captures-with-slopes", "--help"])
    assert " Input file path " in result.stdout
    assert " Output file path " in result.stdout
    assert "[default: " not in result.stdout

    gtt.if_exist_remove(output_path)
    result = runner.invoke(
        app,
        [
            "write-effort-and-captures-with-slopes",
            "--input-path",
            monthly_path,
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0
    gtt.assert_exist(output_path)
    obtained = pd.read_csv(output_path)
    assert obtained.shape[1] == 4

    obtained_slopes = obtained.slope
    expected_slopes = pd.Series(
        [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            4.739e-6,
            -1.28e-5,
            -1.86e-5,
            -9.4e-5,
            3.67e-5,
            11.4e-5,
            5.2e-5,
            2.75e-5,
        ],
        name="slope",
    )
    pd.testing.assert_series_equal(obtained_slopes, expected_slopes, rtol=0.01)
