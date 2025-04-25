import pandas as pd

def calcular_fitness_desde_csv(path_csv="resultados/road_rage_por_step.csv"):
    df = pd.read_csv(path_csv)
    # Media de la métrica compuesta (ya incluye delay, stops, waiting_time y queue_length)
    avg_rage = df["road_rage"].mean()
    # Fitness: queremos minimizar avg_rage, así que:
    fitness = 1.0 - avg_rage
    return round(fitness, 6)
