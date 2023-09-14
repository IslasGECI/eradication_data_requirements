import pandas as pd

from eradication_data_requirements import (
    drop_unused_non_captures,
    get_last_cumsum,
    get_non_captures_index,
    remove_consecutive_non_captures,
    replace_and_drop_non_captures_effort,
    replace_cumulative_non_captures_effort,
    split_non_consecutive_indexes,
)


singular_data = pd.DataFrame(
    {"Esfuerzo": [2, 2, 2, 2, 2, 2, 1, 2, 3], "Capturas": [1, 0, 0, 0, 2, 1, 0, 0, 1]}
)


def test_remove_consecutive_non_captures():
    obtained = remove_consecutive_non_captures(singular_data)
    expected = pd.DataFrame({"Esfuerzo": [2, 6, 2, 2, 3, 3], "Capturas": [1, 0, 2, 1, 0, 1]})
    pd.testing.assert_frame_equal(
        obtained.reset_index(drop=True), expected.reset_index(drop=True), check_dtype=False
    )
    obtained = remove_consecutive_non_captures(expected)
    print(obtained)
    pd.testing.assert_frame_equal(
        obtained.reset_index(drop=True), expected.reset_index(drop=True), check_dtype=False
    )


def test_get_non_captures_index():
    obtained = get_non_captures_index(singular_data)
    expected = [1, 2, 3, 6, 7]
    assert obtained == expected


def test_split_non_consecutive_indexes():
    index_list = [1, 2, 5, 6, 9]
    obtained = split_non_consecutive_indexes(index_list)
    expected = [[1, 2], [5, 6], [9]]
    assert obtained == expected


index_list = [[1, 2, 3], [6, 7]]


def test_get_last_cumsum():
    obtained = get_last_cumsum(singular_data, index_list[0])
    expected_effort = 6
    assert obtained.Esfuerzo == expected_effort


def test_drop_unused_non_captures():
    obtained = drop_unused_non_captures(singular_data, index_list[0])
    expected_length = len(singular_data) - 2
    obtained_length = len(obtained)
    assert obtained_length == expected_length

    index_list_with_one_value = [8]
    obtained = drop_unused_non_captures(singular_data, index_list_with_one_value)
    obtained_length = len(obtained)
    expected_length = len(singular_data)
    assert obtained_length == expected_length


def test_replace_cumulative_non_captures_effort():
    obtained = replace_cumulative_non_captures_effort(singular_data, index_list[1])
    expected_7th_effort = 3
    obtained_7th_effort = obtained.Esfuerzo.loc[7]
    assert obtained_7th_effort == expected_7th_effort


def test_replace_and_drop_non_captures_effort():
    obtained = replace_and_drop_non_captures_effort(singular_data, index_list[1])
    expected_length = len(singular_data) - 1
    obtained_length = len(obtained)
    assert obtained_length == expected_length

    expected_7th_effort = 3
    obtained_7th_effort = obtained.Esfuerzo.loc[7]
    assert obtained_7th_effort == expected_7th_effort
