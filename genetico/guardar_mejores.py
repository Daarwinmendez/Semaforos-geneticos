import json
import os

def guardar_mejores_por_generacion(mejores, carpeta_cont, nombre_json="mejores_por_generacion.json"):
    os.makedirs("resultados", exist_ok=True)
    with open(os.path.join(carpeta_cont, nombre_json), "w") as f:
        json.dump(mejores, f, indent=4)
    print(f"Mejores cromosomas guardados en resultados/{nombre_json}")
