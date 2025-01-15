def combine_distributions_from_dict(pop_status_a, pop_status_b):
    capturas_totales = pop_status_a["capturas"] + pop_status_b["capturas"]
    return {"remanentes": "a (b — c)", "capturas": capturas_totales}
