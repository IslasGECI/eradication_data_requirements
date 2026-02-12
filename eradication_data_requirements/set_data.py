import pandas as pd
from functools import reduce


def filter_data_by_method(raw_data, method):
    filtered_by_method = raw_data[raw_data.Tecnica == method]
    filtered_by_method.loc[:, ["Acumulado"]] = filtered_by_method.Capturas.cumsum()
    return filtered_by_method


def select_month_by_resolution(data, resolution):
    window_length = resolution
    return xxselect_month_by_resolution(data, window_length, resolution)


def xxselect_month_by_resolution(data, window_length, resolution):
    month_to_plot = [f"-{factor:02d}-" for factor in range(1, 13) if factor % resolution == 0]
    mask = reduce(
        lambda x, y: x | y,
        [data["Fecha"].str.contains(pattern, case=False) for pattern in month_to_plot],
    )
    cutted_months = data[mask]
    selected_indexes = pd.concat([cutted_months, data.iloc[-1:]]).index.unique()
    is_index_valid = selected_indexes >= (window_length - 1)
    return selected_indexes[is_index_valid]
