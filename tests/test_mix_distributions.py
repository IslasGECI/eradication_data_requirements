from eradication_data_requirements.mix_distributions import combine_distributions_from_dict
import numpy as np


def test_combine_distributions_from_dict():
    distribution_a = np.random.normal(316, 0.5, 20)
    print(distribution_a)
    pop_status_a = {"distribution": distribution_a, "capturas": 10}
    distribution_a = np.random.normal(316, 0.5, 20)
    pop_status_b = {"distribution": distribution_a, "capturas": 10}
    combine_distributions_from_dict(pop_status_a, pop_status_b)
