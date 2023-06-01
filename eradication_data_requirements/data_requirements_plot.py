import pandas as pd
import numpy as np
from geci_plots import plt, geci_plot


def fit_ramsey_plot(data):
    return np.polyfit(data["Captures"], data["CPUE"], 1)


def data_requirements_plot(input_path, output_path):
    data = pd.read_csv(input_path)
    theta = fit_ramsey_plot(data.drop([0]))
    y_line = theta[1] + theta[0] * data["Captures"]
    fig, ax = geci_plot()
    plt.scatter(data["Captures"], data["CPUE"], marker="o")
    plt.plot(data["Captures"], y_line, "r")
    plt.xlabel("Cumulative captures", size=15, labelpad=15)
    plt.ylabel("CPUE (captures/night traps)", size=15)
    plt.savefig(output_path, dpi=300, transparent=True)
