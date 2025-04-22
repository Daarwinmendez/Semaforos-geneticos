import pandas as pd

def calcular_fitness_desde_csv(path_csv="resultados/road_rage_por_step.csv"):
    df = pd.read_csv(path_csv)
    promedio_rage = df["road_rage"].mean()
    fitness = 1 - promedio_rage  # mientras menos rage, más fitness
    return round(fitness, 6)