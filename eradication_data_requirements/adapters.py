def adapt_effort_and_catpures(data):
    data["Season"] = data["Fecha"].str[:3]
    return data
