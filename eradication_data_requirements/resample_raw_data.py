from bootstrapping_tools import resample_data


def resample_valid_data(effort_and_capture_data, seed):
    return resample_data(effort_and_capture_data, seed, blocks_length=2)
