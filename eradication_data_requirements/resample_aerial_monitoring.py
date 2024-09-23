from bootstrapping_tools import resample_data


def get_sum_distribution(df, bootstrap_number):
    blocks_length = 1
    return [resample_data(df, seed, blocks_length) for seed in range(bootstrap_number)]
