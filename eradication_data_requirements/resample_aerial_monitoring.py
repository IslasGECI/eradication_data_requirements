from bootstrapping_tools import resample_data


def get_sum_distribution(df, bootstrap_number):
    blocks_length = 1
    return [
        int(resample_data(df, seed, blocks_length).No_goats.sum())
        for seed in range(bootstrap_number)
    ]
