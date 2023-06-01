import os
import eradication_data_requirements as dt


def test_data_requirements_plot():
    input_path = "/workdir/tests/data/cumulative_effort_and_captures_for_year.csv"
    output_path = "/workdir/tests/data/yearly_ramsy_plot.png"
    if os.path.exists(output_path):
        os.remove(output_path)
    dt.data_requirements_plot(input_path, output_path)
    pass
