import numpy as np

from eradication_data_requirements.data_requirements_plot import fit_ramsey_plot
from eradication_data_requirements.calculate_intersect import resample_eradication_data


def get_slopes_distribution(raw_data, bootstrap_number):
    rng = np.random.default_rng()
    return [get_slope(resample_eradication_data(raw_data, rng)) for _ in range(bootstrap_number)]


def get_slope(data):
    parameters = fit_ramsey_plot(data)
    return parameters[0]
