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

#correr_simulacion("Escenarios/1. Zona Universitaria (UASD)/osm.sumocfg")
path = "Escenarios/1. Zona Universitaria (UASD)/osm.sumocfg"
correr_simulacion_limited(cfg_path=path, steps=200)