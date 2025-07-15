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
