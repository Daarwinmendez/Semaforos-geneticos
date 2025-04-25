import pandas as pd
import os

def guardar_benchmark_generacion(lista_fitness, carpeta_cont, nombre_csv="benchmark_generaciones.csv"): 
    """
    Recibe una lista de dicts con fitness por generación y guarda un CSV resumen.
    """
    os.makedirs("resultados", exist_ok=True) # Crear carpeta de resultados si no existe
    df = pd.DataFrame(lista_fitness)  # Convertir a DataFrame
    df.to_csv(os.path.join(carpeta_cont, nombre_csv), index=False)  # Guardar en carpeta de generación
    print(f"Benchmark guardado en resultados/{nombre_csv}") 
