import json, random
from pathlib import Path

def seleccionar_padres_probabilidad(
        path_resultados_json: str,
        k: int,
        rnd: random.Random | None = None
    ) -> list[dict]:
    """
    Devuelve `k` cromosomas elegidos por ruleta (fitness-proportional).

    Args
    ----
    path_resultados_json : str
        Archivo con los resultados de la generación (fitness + cromosoma).
    k : int
        Nº de individuos a seleccionar.
    rnd : random.Random | None
        Objeto Random para reproducibilidad externa (opcional).
    """
    if rnd is None:
        rnd = random

    resultados = json.loads(Path(path_resultados_json).read_text(encoding="utf-8"))

    # extraer fitness y desplazar si hay valores <= 0 
    fitness = [r["fitness"] for r in resultados]
    min_fit = min(fitness)
    if min_fit <= 0:
        fitness = [f - min_fit + 1e-6 for f in fitness]   # evita probs 0/negativas

    total = sum(fitness)
    probs = [f / total for f in fitness]

    indices = rnd.choices(range(len(resultados)), weights=probs, k=k)
    padres = [resultados[i]["cromosoma"] for i in indices]

    rate = k / len(resultados)
    print(f"[INFO] Seleccionados {k} individuos por probabilidad "
          f"(selection_rate = {rate:.2f})")

    return padres
