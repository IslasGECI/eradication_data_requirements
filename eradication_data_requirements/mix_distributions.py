import numpy as np


def combine_distributions_from_dict(pop_status_a, pop_status_b):
    capturas_totales = pop_status_a["capturas"] + pop_status_b["capturas"]
    return {"remanentes": "a (b — c)", "capturas": capturas_totales}


def concatenate_remanent_distributions(pop_status_a, pop_status_b):
    n0_a = pop_status_a["distribution"]
    n0_b = pop_status_b["distribution"]
    return np.concatenate((n0_a, n0_b))
