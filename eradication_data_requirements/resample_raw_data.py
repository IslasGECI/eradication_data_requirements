from bootstrapping_tools import resample_data


def resample_valid_data(effort_and_capture_data, seed):
    sample = resample_data(effort_and_capture_data, seed, blocks_length=2)
    return validate_samples_to_fit([sample])


def validate_samples_to_fit(samples):
    validated = [
        valid_sample
        for valid_sample in samples
        if len(valid_sample.Capturas.unique()) > 1
        and valid_sample.Capturas.sum() != valid_sample.Capturas[0]
    ]
    return validated