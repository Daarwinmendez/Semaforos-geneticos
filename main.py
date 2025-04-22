import traci
import json
import os

'''iteration = 1
os.makedirs("configs/Semaforos/", exist_ok=True)
os.makedirs(f"configs/Semaforos/iter_{iteration}", exist_ok=True)

traci.start(["sumo-gui", "-c", "Escenarios/1. Zona Universitaria (UASD)/osm.sumocfg"])
traci.simulationStep()

traffic_lights = traci.trafficlight.getIDList()

for tls_id in traffic_lights:
    configs = traci.trafficlight.getAllProgramLogics(tls_id)

    config_serializable = []
    for logic in configs:
        config_serializable.append({
            "id": tls_id,
            "type": logic.type,
            "programID": logic.programID,
            "offset": getattr(logic, "offset", 0),  # ← CAMBIADO AQUÍ
            "phases": [
                {
                    "duration": phase.duration,
                    "state": phase.state,
                    "minDur": getattr(phase, "minDur", None),
                    "maxDur": getattr(phase, "maxDur", None)
                }
                for phase in logic.phases
            ]
        })

    
    with open(f"configs/Semaforos/iter_{iteration}/{tls_id}.json", "w") as f:
        json.dump(config_serializable, f, indent=4)

# Continuar simulaciónc
for step in range(1000):
    traci.simulationStep()
    for v in traci.vehicle.getIDList():
        print(f"{v}: {traci.vehicle.getPosition(v)}")

traci.close()
'''


from simulacion.controlador import correr_simulacion, correr_simulacion_limited
from utils.analisis_road_rage import analizar_road_rage
from utils.resumen_por_semaforo import resumen_por_semaforo


#correr_simulacion("Escenarios/1. Zona Universitaria (UASD)/osm.sumocfg")
path = "Escenarios/1. Zona Universitaria (UASD)/osm.sumocfg"
correr_simulacion_limited(cfg_path=path, steps=200)
analizar_road_rage(path_csv="resultados/metrics_test.csv", salida_csv="resultados/road_rage_por_step.csv")
resumen_por_semaforo(path_csv="resultados/metrics_test.csv", salida_csv="resultados/resumen_semaforos.csv")
