import copy
import random

def crossover_cromosomas(padre1, padre2):
    """
    Realiza crossover entre dos cromosomas y devuelve un nuevo hijo.
    Para cada semáforo, escoge aleatoriamente la configuración de uno de los padres.
    """
    hijo = {}
    for s_id in padre1:
        # Coin toss: 0 → padre1, 1 → padre2
        if random.random() < 0.5:
            hijo[s_id] = copy.deepcopy(padre1[s_id])
        else:
            hijo[s_id] = copy.deepcopy(padre2[s_id])
    return hijo

def mutar_cromosoma(cromosoma, prob_mutacion=0.7):
    import copy, random, pprint
    crom_mutado = copy.deepcopy(cromosoma)
    for s_id, config in crom_mutado.items():
        offset_orig = config.get("offset", None)
        # Mutar offset
        if "offset" in config and random.random() < prob_mutacion:
            config["offset"] = random.randint(0, 30)
            print(f"Mutado offset de {s_id}: {offset_orig} -> {config['offset']}")
        # Mutar CADA fase con cierta probabilidad
        if "phases" in config:
            for fase_idx, fase in enumerate(config["phases"]):
                dur_orig = fase.get("duration", None)
                min_dur = fase.get("minDur", 5)
                max_dur = fase.get("maxDur", 50)
                if min_dur is None: min_dur = 5
                if max_dur is None: max_dur = 50
                if "duration" in fase and random.random() < prob_mutacion:
                    fase["duration"] = round(random.uniform(min_dur, max_dur), 1)
                    print(f"Mutado duration en {s_id} (fase {fase_idx}): {dur_orig} -> {fase['duration']}")
    print("Cromosoma mutado:")
    pprint.pprint(crom_mutado)
    return crom_mutado