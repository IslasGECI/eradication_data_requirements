def adapt_effort_and_catpures(data):
    data["Season"] = data["Fecha"].str[:4]
    return data
