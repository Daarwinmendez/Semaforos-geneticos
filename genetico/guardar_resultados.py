import json
import os

def guardar_resultados_generacion(resultados, nombre_archivo="resultados_generacion_1.json"):
    """
    Guarda la lista de resultados (fitness, cromosoma, etc) en la carpeta 'resultados' como JSON.
    """
    os.makedirs("resultados", exist_ok=True)
    path = os.path.join("resultados", nombre_archivo)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4)
    print(f"Resultados de la generación guardados en {path}")
