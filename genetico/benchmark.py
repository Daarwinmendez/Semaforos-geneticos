import pandas as pd
import os

def guardar_benchmark_generacion(lista_fitness, nombre_csv="benchmark_generaciones.csv"):
    """
    Recibe una lista de dicts con fitness por generación y guarda un CSV resumen.
    """
    os.makedirs("resultados", exist_ok=True)
    df = pd.DataFrame(lista_fitness)  # ← Aquí no uses read_csv, solo DataFrame directo
    df.to_csv(os.path.join("resultados", nombre_csv), index=False)
    print(f"Benchmark guardado en resultados/{nombre_csv}")
