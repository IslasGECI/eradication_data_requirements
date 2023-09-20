import numpy as np
import pandas as pd


from eradication_data_requirements.data_requirements_plot import fit_ramsey_plot
from eradication_data_requirements.resample_raw_data import resample_valid_data


def add_slopes_to_effort_capture_data(data):
    ramsey_time_series = set_up_ramsey_time_series(data)
    slopes_and_intercept = calculate_six_months_slope(ramsey_time_series)
    slopes_status = extract_slopes(slopes_and_intercept)
    ramsey_time_series = paste_status(ramsey_time_series, slopes_status, "slope")
    return ramsey_time_series


def add_probs_to_effort_capture_data(data_copy, bootstrapping_number):
    resized_data = data_copy[data_copy.Esfuerzo != 0]
    samples = calculate_resampled_six_months_slope(resized_data, bootstrapping_number)
    probs_status = extract_prob(samples)
    resized_data = paste_status(resized_data, probs_status, "prob")
    return resized_data[["Fecha", "Esfuerzo", "Capturas", "prob"]]


def paste_status(data_copy, probs_status, column_name):
    df = add_empty_column(data_copy, column_name)
    assert len(df.loc[5:, column_name]) == len(probs_status), "Different dimensions"
    df.loc[5:, column_name] = probs_status
    return df


def add_empty_column(data_copy, column_name):
    df_copy = data_copy.copy()
    df_copy.loc[:, column_name] = np.nan
    return df_copy


def set_up_ramsey_time_series(data):
    cumulative_captures = pd.DataFrame()
    cumulative_captures["Fecha"] = data.Fecha
    cumulative_captures["Cumulative_captures"] = data["Capturas"].cumsum()
    cumulative_captures["CPUE"] = data["Capturas"] / data["Esfuerzo"]
    return cumulative_captures[["Fecha", "CPUE", "Cumulative_captures"]]


def resample_fit_ramsey_plot(datos, bootstrapping_number):
    resampled_data = resample_valid_data(datos, bootstrapping_number)
    ramsey_series = [set_up_ramsey_time_series(sample) for sample in resampled_data]
    fits = [fit_ramsey_plot(ramsey_serie) for ramsey_serie in ramsey_series]
    return fits


def calculate_resampled_six_months_slope(ramsey_series, bootstrapping_number):
    window_length = 6
    return [
        resample_fit_ramsey_plot(ramsey_series.iloc[(i - window_length) : i], bootstrapping_number)
        for i in range(window_length, len(ramsey_series) + 1)
    ]


def calculate_six_months_slope(data):
    window_length = 6
    return [
        fit_ramsey_plot(data.iloc[(i - window_length) : i])
        for i in range(window_length, len(data) + 1)
    ]


def extract_slopes(slopes_intercept_data):
    return [slope[0] for slope in slopes_intercept_data]


def extract_prob(slopes_intercept_data):
    slopes = [np.asarray(extract_slopes(sample)) for sample in slopes_intercept_data]
    return [np.mean(samples < 0) for samples in slopes]
