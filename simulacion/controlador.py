import traci
from simulacion.metrics_logger import MetricsLogger
from simulacion.metrics import calcular_retraso_vehiculo
import os
import json

def aplicar_configuracion_cromosoma(carpeta_config):
    for archivo in os.listdir(carpeta_config):
        if archivo.endswith(".json"):
            path = os.path.join(carpeta_config, archivo)
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
                if isinstance(config, list):
                    print(f"[INFO] Archivo {archivo} es una lista (cluster); ignorado.")
                    continue
                tls_id = config["id"]
                phases = []
                for fase in config["phases"]:
                    duration = round(fase["duration"])
                    state = fase["state"]
                    minDur = int(fase.get("minDur", duration))
                    maxDur = int(fase.get("maxDur", duration))
                    phases.append(traci.trafficlight.Phase(duration, state, minDur, maxDur))
                logic = traci.trafficlight.Logic(
                    config["programID"],
                    int(config.get("type", 0)),
                    0,  # currentPhaseIndex
                    phases
                )
                # Usa la función recomendada (soporta ambos nombres en versiones nuevas)
                traci.trafficlight.setProgramLogic(tls_id, logic)
                print(f"[✔] Aplicado TLS {tls_id} | fases={len(config['phases'])}")

def correr_simulacion_limited(cfg_path, steps=500, salida="resultados/metrics_test.csv", carpeta_config="configs/Semaforos/iter_1"):
    print("Iniciando simulación limitada...")
    traci.start(["sumo", "-c", cfg_path])

    aplicar_configuracion_cromosoma(carpeta_config)  # <- Aplicamos configuración antes de simular

    semaforos = traci.trafficlight.getIDList()
    logger = MetricsLogger(semaforo_ids=semaforos)

    step = 0
    while traci.simulation.getMinExpectedNumber() > 0 and step < steps:
        traci.simulationStep()
        logger.update(step)
        print(f"Step: {step}")
        step += 1

    traci.close()
    logger.export_to_csv(salida)
    print(f"Simulación completada. Resultados exportados a: {salida}")
