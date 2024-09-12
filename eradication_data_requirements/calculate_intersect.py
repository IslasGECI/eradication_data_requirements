import numpy as np
from bootstrapping_tools import generate_latex_interval_string
from eradication_data_requirements import fit_ramsey_plot


def calculate_intercept_interval(distribution):
    interval = np.percentile(distribution, [2.5, 50, 97.5]).astype(int)
    latex_string = generate_latex_interval_string(interval, deltas=False, decimals=0)
    return latex_string


def get_intercepts_distribution(raw_data, bootstrap_number, seed=None):
    rng = np.random.default_rng(seed)
    return [
        calculate_x_intercept(resample_eradication_data(raw_data, rng))
        for _ in range(bootstrap_number)
    ]


def resample_eradication_data(data, rng):
    resampled_data = data.sample(replace=True, frac=1, random_state=rng)
    resampled_data["Cumulative_captures"] = data.Capturas.cumsum()
    return resampled_data[["CPUE", "Cumulative_captures"]]


def calculate_x_intercept(data):
    parameters = fit_ramsey_plot(data)
    return -parameters[1] / parameters[0]
