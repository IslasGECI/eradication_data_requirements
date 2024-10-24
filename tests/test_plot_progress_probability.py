from eradication_data_requirements import plot_progress_probability

import pandas as pd
import matplotlib as plt


def test_plot_progress_probability():
    data = pd.read_csv("tests/data/progress_probability_tests.csv")
    obtained = plot_progress_probability(data)
    assert isinstance(obtained, plt.axes._axes.Axes)

    obtained_y_label = obtained.get_ylabel()
    expected_y_label = "Progress probability"
    assert obtained_y_label == expected_y_label

    obtained_ylim = plt.pyplot.ylim()
    expected_ylim = (-0.05, 1.05)
    assert obtained_ylim == expected_ylim
    assert obtained.get_xticklabels()[0].get_text() == "2015-07"
    assert obtained.get_xticklabels()[1].get_text() == "2016-03"
    assert obtained.get_xticklabels()[1].get_rotation() == 90.0
    assert obtained.get_yaxis().get_label().get_fontsize() == 20.0
