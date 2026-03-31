import matplotlib.pyplot as plt
from eradication_data_requirements.calculate_intersect import add_cpue
from eradication_data_requirements.fit_ramsey_plot import fit_ramsey_plot

from geci_plots import geci_plot


def plot_comparative_catch_curves(socorro_data, guadalupe_data):
    _, ax = geci_plot()
    ax = plot_catch_curve(socorro_data, ax, "Socorro")
    ax = plot_catch_curve(guadalupe_data, ax, "Guadalupe")
    plt.xlabel("Cumulative captures", size=15, labelpad=15)
    plt.ylabel("CPUE (captures/night traps)", size=15)
    plt.legend(fontsize="xx-large")
    return ax


def plot_traps_data_requirements(data):
    config_plot = {"ylabel": "CPUE (captures/night traps)", "cumulative": "Cumulative_captures"}
    return data_requirements_plot(data, config_plot)


def data_requirements_plot(data, config_plot):
    configured_data = set_cumulative_captures_column(data, config_plot)
    _, ax = geci_plot()
    ax = plot_catch_curve(configured_data, ax)
    plt.xlabel("Cumulative captures", size=15, labelpad=15)
    plt.ylabel(config_plot["ylabel"], size=15)
    return ax


def set_cumulative_captures_column(data, config):
    return data.rename(columns=config)


def plot_catch_curve(data, ax, label=None):
    theta = fit_ramsey_plot(data)
    y_line = theta[1] + theta[0] * data["Cumulative_captures"]
    ax.plot(data["Cumulative_captures"], y_line, "r")
    ax.scatter(data["Cumulative_captures"], data["CPUE"], marker="o", label=label)
    return ax
