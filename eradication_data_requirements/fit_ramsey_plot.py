import numpy as np
import warnings


def fit_ramsey_plot(data):
    try:
        fit = np.polynomial.polynomial.Polynomial.fit(
            data["Cumulative_captures"], data["CPUE"], deg=1
        )
        intercept_and_slope = fit.convert().coef
        idx = [1, 0]
        slope_and_intercept = intercept_and_slope[idx]
    except (AssertionError, IndexError):
        warnings.warn("Error")
        slope_and_intercept = [np.nan, np.nan]
    return slope_and_intercept
