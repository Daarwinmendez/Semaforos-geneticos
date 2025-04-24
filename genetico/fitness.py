import pandas as pd

def calcular_fitness_desde_csv(path_csv="resultados/road_rage_por_step.csv"):
    df = pd.read_csv(path_csv)
    avg_rage = df["road_rage"].mean()
    avg_delay = df["delay"].mean()
    avg_stops = df["stops"].mean()
    # Ajusta los pesos según lo que quieres optimizar
    fitness = 1 - (0.5 * avg_rage + 0.3 * avg_delay/10 + 0.2 * avg_stops/5)
    return round(fitness, 6)