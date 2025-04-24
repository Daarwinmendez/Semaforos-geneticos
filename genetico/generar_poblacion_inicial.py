import os
import json
import random
from copy import deepcopy

def generar_poblacion_inicial(carpeta_semaforos, n_pobladores=10, seed=None):
    """
    Lee todos los JSON de configuraciones de semáforos individuales de una carpeta,
    y genera una población de cromosomas aleatorios (dictionaries con las fases randomizadas).
    Solo toma archivos con nombres numéricos (evita clusters).
    """
    if seed is not None:
        random.seed(seed)

    archivos = [
        f for f in os.listdir(carpeta_semaforos)
        if f.endswith('.json') and f.split('.')[0].isdigit()
    ]
    plantillas = {}
    for archivo in archivos:
        with open(os.path.join(carpeta_semaforos, archivo), 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Si el JSON es una lista, tomar el primer elemento
            if isinstance(data, list):
                data = data[0]
            plantillas[data["id"]] = data  # key: semaforo id

    poblacion = []
    for _ in range(n_pobladores):
        cromosoma = {}
        for s_id, plantilla in plantillas.items():
            # Hacer deep copy de la estructura base
            config = deepcopy(plantilla)
            # Randomizar duration (y offset si lo deseas)
            for fase in config["phases"]:
                min_dur = fase.get("minDur", 5)
                max_dur = fase.get("maxDur", 50)
                if min_dur is None: min_dur = 5
                if max_dur is None: max_dur = 50
                if "duration" in fase:
                    fase["duration"] = round(random.uniform(min_dur, max_dur), 1)
            # Offset aleatorio (puedes modificar el rango si quieres)
            if "offset" in config:
                config["offset"] = random.randint(0, 30)
            cromosoma[s_id] = config
        poblacion.append(cromosoma)
    return poblacion

# Ejemplo de uso directo:
if __name__ == "__main__":
    poblacion = generar_poblacion_inicial(r"C:\Users\micha\OneDrive\Documentos\Cosas-de-la-Uni\Tareas-y-Trabajos-de-IA-Distribuida\-Proyectos-de-DAI\Proyecto Final\Semaforos-geneticos\configs\Semaforos\iter_1", n_pobladores=3)
    import pprint
    pprint.pprint(poblacion[0])