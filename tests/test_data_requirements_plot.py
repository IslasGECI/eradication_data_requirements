import os
import hashlib
import pandas as pd
import numpy as np
import pytest

import eradication_data_requirements as dt


def test_data_requirements_plot():
    input_path = "/workdir/tests/data/cumulative_effort_and_captures_for_year.csv"
    output_path = "/workdir/tests/data/yearly_ramsey_plot.png"
    remove_file_if_exists(output_path)
    dt.data_requirements_plot(input_path, output_path)
    file_content = open(output_path, "rb").read()
    obtained_hash = hashlib.md5(file_content).hexdigest()
    expected_hash = "0f6baede0ee8e01974f01e2109e81535"
    assert obtained_hash == expected_hash
    remove_file_if_exists(output_path)


def remove_file_if_exists(output_path):
    if os.path.exists(output_path):
        os.remove(output_path)


def test_fit_ramsey_plot():
    data = pd.DataFrame(
        {"CPUE": [19.5, 19, 18.5, 18, 17.5, 17], "Cumulative_captures": [1, 2, 3, 4, 5, 6]}
    )
    obtained_parameters = dt.fit_ramsey_plot(data)
    expected_parameters = np.array([-0.5, 20.0])
    np.testing.assert_array_almost_equal(obtained_parameters, expected_parameters)

    data_error = pd.DataFrame(
        {"CPUE": [19.5, 19, 18.5, 18, 17.5, 17], "Cumulative_captures": [1, 1, 1, 1, 1, 1]}
    )
    with pytest.raises(AssertionError, match=r"^It can not fit Ramsey plot$"):
        dt.fit_ramsey_plot(data_error)

    data_without_error = pd.DataFrame(
        {"CPUE": [19.5, 19, 18.5, 18, 17.5, 17], "Cumulative_captures": [1, 1, 1, 1, 1, 2]}
    )
    assert isinstance(dt.fit_ramsey_plot(data_without_error), type(np.array(0)))
