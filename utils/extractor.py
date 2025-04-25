# utils/extractor.py
import traci
import os
import json

def extraer_configuraciones_semaforos(cfg_path, carpeta_salida):
    os.makedirs(carpeta_salida, exist_ok=True)
    traci.start(["sumo", "-c", cfg_path])
    traci.simulationStep()
    traffic_lights = traci.trafficlight.getIDList()
    for tls_id in traffic_lights:
        configs = traci.trafficlight.getAllProgramLogics(tls_id)
        for logic in configs:
            path = os.path.join(carpeta_salida, f"{tls_id}.json")
            config_dict = {
                "id": tls_id,
                "type": logic.type,
                "programID": logic.programID,
                "offset": getattr(logic, "offset", 0),
                "phases": [
                    {
                        "duration": phase.duration,
                        "state": phase.state,
                        "minDur": getattr(phase, "minDur", None),
                        "maxDur": getattr(phase, "maxDur", None)
                    }
                    for phase in logic.phases
                ]
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=4)
    traci.close()
    print(f"[INFO] Configuración base extraída y guardada en {carpeta_salida}")
