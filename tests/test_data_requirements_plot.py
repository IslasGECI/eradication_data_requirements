import os
import hashlib
import eradication_data_requirements as dt


def test_data_requirements_plot():
    input_path = "/workdir/tests/data/cumulative_effort_and_captures_for_year.csv"
    output_path = "/workdir/tests/data/yearly_ramsy_plot.png"
    if os.path.exists(output_path):
        os.remove(output_path)
    dt.data_requirements_plot(input_path, output_path)
    file_content = open(output_path, "rb").read()
    obtained_hash = hashlib.md5(file_content).hexdigest()
    expected_hash = "145db61b30a8246e9563378d1db5cf7e"
    assert obtained_hash == expected_hash
