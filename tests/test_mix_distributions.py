from eradication_data_requirements.mix_distributions import (
    combine_distributions_from_dict,
    concatenate_remanent_distributions,
)
import numpy as np


rng = np.random.default_rng(seed=42)
distribution_a = rng.normal(316, 5, 20)
print(distribution_a)
pop_status_a = {"distribution": distribution_a, "capturas": 20}
distribution_b = rng.normal(100, 10, 20)
print(distribution_b)
pop_status_b = {"distribution": distribution_b, "capturas": 10}


def test_combine_distributions_from_dict():
    obtained = combine_distributions_from_dict(pop_status_a, pop_status_b)
    assert "remanentes" in obtained.keys()
    assert obtained["remanentes"] == "199 (82 - 301)"
    assert len(obtained["remanentes_distribution"]) == len(distribution_a) + len(distribution_b)
    assert obtained["capturas"] == 30


def test_concatenate_remanent_distributions():
    obtained = concatenate_remanent_distributions(pop_status_a, pop_status_b)
    expected_len = len(distribution_b) + len(distribution_a)
    assert len(obtained) == expected_len
    assert max(obtained) < max(distribution_a)
