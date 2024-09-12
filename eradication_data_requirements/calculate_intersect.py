import numpy as np

from eradication_data_requirements import fit_ramsey_plot


def get_intercepts_distribution(raw_data, bootstrap_number, seed=2):
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
