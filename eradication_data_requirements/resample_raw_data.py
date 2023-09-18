from bootstrapping_tools import resample_data


def resample_valid_data(effort_and_capture_data, bootstrapping_number):
    blocks_length = 2
    sample = [
        resample_data(effort_and_capture_data, seed, blocks_length)
        for seed in range(bootstrapping_number)
    ]
    return validate_samples_to_fit(sample)


def validate_samples_to_fit(samples):
    validated = [
        valid_sample
        for valid_sample in samples
        if valid_sample.Capturas.sum() != valid_sample.Capturas[0]
    ]
    return validated
