import json
import os
from pathlib import Path

def guardar_resultados_generacion(resultados, nombre_archivo: str) -> None:
    """
    Guarda la lista `resultados` en la ruta indicada por `nombre_archivo`.

    • Si `nombre_archivo` incluye carpeta, se respeta tal cual.
    • Si solo es un nombre (sin separadores), se guarda en la carpeta
      'resultados/' por compatibilidad con el uso original.
    """
    # ¿incluye folder?  ->  ruta completa
    if os.sep in nombre_archivo or "/" in nombre_archivo:
        path = Path(nombre_archivo)
    else:
        path = Path("resultados") / nombre_archivo

    # crea carpetas si hicieran falta
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4)

    print(f"[OK] Resultados de la generación guardados en {path}")
