import traci
from simulacion.metrics_logger import MetricsLogger
from simulacion.metrics import calcular_retraso_vehiculo

def correr_simulacion(cfg_path):
    traci.start(["sumo-gui", "-c", cfg_path])

    semaforos = traci.trafficlight.getIDList()
    logger = MetricsLogger(semaforo_ids=semaforos)

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step = traci.simulation.getTime()
        logger.update(step)

    traci.close()
    logger.export_to_csv("resultados/metrics_por_step.csv")

def correr_simulacion_multiples(cfg_path):
    traci.start(["sumo-gui", "-c", cfg_path])

    semaforos = traci.trafficlight.getIDList()
    semaforo_pos_dict = {
        tls_id: traci.lane.getShape(traci.trafficlight.getControlledLanes(tls_id)[0])[-1]
        for tls_id in semaforos
    }

    delay_por_tls = {tls_id: [] for tls_id in semaforos}

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        for veh_id in traci.vehicle.getIDList():
            for tls_id, semaforo_pos in semaforo_pos_dict.items():
                delay = calcular_retraso_vehiculo(veh_id, semaforo_pos)
                if delay is not None:
                    delay_por_tls[tls_id].append(delay)

    traci.close()

    resultados = {
        tls_id: (sum(delays) / len(delays) if delays else None)
        for tls_id, delays in delay_por_tls.items()
    }
    return resultados

def correr_simulacion_limited(cfg_path, steps=500, salida="resultados/metrics_test.csv"):
    print("Iniciando simulación limitada...")
    traci.start(["sumo-gui", "-c", cfg_path])

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