import os
import hashlib
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
