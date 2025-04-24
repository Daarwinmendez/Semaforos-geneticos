import json

def seleccionar_elite(path_resultados_json, n_elite=2):
    """
    Carga los resultados de una generación y retorna los N mejores cromosomas (elite) ordenados por fitness.
    """
    with open(path_resultados_json, "r", encoding="utf-8") as f:
        resultados = json.load(f)
    # Ordenar por fitness (mayor es mejor)
    resultados_ordenados = sorted(resultados, key=lambda x: x["fitness"], reverse=True)
    elite = resultados_ordenados[:n_elite]
    print(f"Top {n_elite} cromosomas (elite):")
    for i, entry in enumerate(elite):
        print(f"Rank {i+1}: Fitness = {entry['fitness']:.4f}")
    return elite
