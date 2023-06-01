import os
import hashlib
import pandas as pd
import numpy as np

import eradication_data_requirements as dt


def test_data_requirements_plot():
    input_path = "/workdir/tests/data/cumulative_effort_and_captures_for_year.csv"
    output_path = "/workdir/tests/data/yearly_ramsey_plot.png"
    if os.path.exists(output_path):
        os.remove(output_path)
    dt.data_requirements_plot(input_path, output_path)
    file_content = open(output_path, "rb").read()
    obtained_hash = hashlib.md5(file_content).hexdigest()
    expected_hash = "3ac61e336449f0f96c83cb2b11b86101"
    assert obtained_hash == expected_hash
    if os.path.exists(output_path):
        os.remove(output_path)


def test_fit_ramsey_plot():
    data = pd.DataFrame(
        {"CPUE": [19.5, 19, 18.5, 18, 17.5, 17], "Cumulative_captures": [1, 2, 3, 4, 5, 6]}
    )
    obtained_parameters = dt.xxfit_ramsey_plot(data)
    expected_parameters = np.array([-0.5, 20.0])
    np.testing.assert_array_almost_equal(obtained_parameters, expected_parameters)
