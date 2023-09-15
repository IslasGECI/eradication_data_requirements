from eradication_data_requirements import plot_progress_probability

import pandas as pd
import matplotlib as plt


def test_plot_progress_probability():
    data = pd.read_csv("tests/data/progress_probability_tests.csv")
    obtained = plot_progress_probability(data)
    assert isinstance(obtained, plt.axes._axes.Axes)
