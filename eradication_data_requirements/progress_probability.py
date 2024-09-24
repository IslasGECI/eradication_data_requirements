from eradication_data_requirements.data_requirements_plot import fit_ramsey_plot


def get_slope(data):
    parameters = fit_ramsey_plot(data)
    return parameters[0]
