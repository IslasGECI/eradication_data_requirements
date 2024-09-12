from eradication_data_requirements import fit_ramsey_plot


def get_intercepts_distribution(raw_data, bootstrap_number):
    return [
        calculate_x_intercept(resample_eradication_data(raw_data)) for _ in range(bootstrap_number)
    ]


def resample_eradication_data(data):
    resampled_data = data.sample(replace=True, frac=1)
    resampled_data["Cumulative_captures"] = data.Capturas.cumsum()
    return resampled_data[["CPUE", "Cumulative_captures"]]


def calculate_x_intercept(data):
    parameters = fit_ramsey_plot(data)
    return -parameters[1] / parameters[0]
