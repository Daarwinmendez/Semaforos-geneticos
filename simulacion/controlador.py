import os, json, random
import traci
from simulacion.metrics_logger import MetricsLogger

# Aplicación de la configuración de un cromosoma a un semáforo en SUMO
def aplicar_configuracion_cromosoma(carpeta_config: str) -> None:
    """
    Lee los JSON generados por el AG y aplica la lógica estática completa
    (duraciones + offset) a cada semáforo mediante TraCI.
    """
    for archivo in os.listdir(carpeta_config):
        if not archivo.endswith(".json"):
            continue

        with open(os.path.join(carpeta_config, archivo), encoding="utf-8") as f:
            cfg = json.load(f)

        # ignorar clusters
        if isinstance(cfg, list):
            continue

        tls_id = cfg["id"]
        offset = int(cfg.get("offset", 0))

        # obligamos a lógica ESTÁTICA
        phases = []
        for fase in cfg["phases"]:
            dur = round(fase["duration"])
            state = fase["state"]
            phases.append(
                traci.trafficlight.Phase(
                    dur,              
                    state,             
                    dur,               
                    dur                
                )
            )

        logic = traci.trafficlight.Logic(
            programID=str(cfg.get("programID", 0)),
            type=0,
            currentPhaseIndex=0,
            phases=phases
        )
        setattr(logic, "offset", offset) 
        traci.trafficlight.setProgramLogic(tls_id, logic)

        print(f"[✔] TLS {tls_id} aplicado | offset={offset} | fases={[p.duration for p in phases]}")


# Corre la simulación de SUMO con la configuración de un cromosoma
def correr_simulacion_limited(
        cfg_path: str,
        steps: int = 500,
        salida: str = "resultados/metrics_test.csv",
        carpeta_config: str | None = None,
        seed: int | None = None
    ) -> None:
    """
    Lanza SUMO headless con una semilla aleatoria (o la que se indique),
    aplica el cromosoma y registra las métricas hasta `steps` pasos.
    """
    if seed is None:
        seed = random.randint(1, 10**6)

    traci.start(["sumo", "-c", cfg_path, "--seed", str(seed), "--no-step-log", "true"])
    print(f"[INFO] SUMO iniciado con seed={seed}")

    if carpeta_config:
        aplicar_configuracion_cromosoma(carpeta_config)

    semaforos = traci.trafficlight.getIDList()
    logger = MetricsLogger(semaforo_ids=semaforos)

    for step in range(steps):
        if traci.simulation.getMinExpectedNumber() == 0:
            break
        traci.simulationStep()
        logger.update(step)

    traci.close()
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    logger.export_to_csv(salida)
    print(f"[OK] Simulación cerrada. CSV en {salida}")
