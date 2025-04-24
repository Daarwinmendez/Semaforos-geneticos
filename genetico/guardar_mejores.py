import json
import os

def guardar_mejores_por_generacion(mejores, nombre_json="mejores_por_generacion.json"):
    os.makedirs("resultados", exist_ok=True)
    with open(os.path.join("resultados", nombre_json), "w", encoding="utf-8") as f:
        json.dump(mejores, f, indent=4)
    print(f"Mejores cromosomas guardados en resultados/{nombre_json}")
