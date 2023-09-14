from itertools import groupby
from operator import itemgetter


def remove_consecutive_non_captures(data):
    data_copy = data.copy()
    non_captures_indexes = get_non_captures_index(data)
    indexes_list = split_non_consecutive_indexes(non_captures_indexes)
    for index_list in indexes_list:
        data_copy = replace_and_drop_non_captures_effort(data_copy, index_list)
    return data_copy


def replace_and_drop_non_captures_effort(data, index_list):
    data_with_cumulative_effort = replace_cumulative_non_captures_effort(data, index_list)
    return drop_unused_non_captures(data_with_cumulative_effort, index_list)


def replace_cumulative_non_captures_effort(singular_data, index_list):
    last_cumsum = get_last_cumsum(singular_data, index_list)
    last_index = index_list[-1]
    singular_data_copy = singular_data.copy()
    singular_data_copy.loc[last_index, "Esfuerzo"] = last_cumsum.Esfuerzo
    return singular_data_copy


def get_last_cumsum(singular_data, index_list):
    return singular_data.loc[index_list].cumsum().iloc[-1]


def split_non_consecutive_indexes(index_list):
    return [
        list(map(itemgetter(1), g))
        for k, g in groupby(enumerate(index_list), lambda i_x: i_x[0] - i_x[1])
    ]


def get_non_captures_index(data):
    return data.index[data.Capturas == 0].to_list()


def drop_unused_non_captures(data, non_captures_indexes):
    return data.drop(non_captures_indexes[:-1])
