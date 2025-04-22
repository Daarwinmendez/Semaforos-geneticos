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

    # Diccionario de posiciones de semáforos
    semaforos = traci.trafficlight.getIDList()
    semaforo_pos_dict = {}

    for tls_id in semaforos:
        lane_id = traci.trafficlight.getControlledLanes(tls_id)[0]
        semaforo_pos_dict[tls_id] = traci.lane.getShape(lane_id)[-1]

    delay_por_tls = {tls_id: [] for tls_id in semaforos}

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        for veh_id in traci.vehicle.getIDList():
            for tls_id, semaforo_pos in semaforo_pos_dict.items():
                delay = calcular_retraso_vehiculo(veh_id, semaforo_pos)
                if delay is not None:
                    delay_por_tls[tls_id].append(delay)

    traci.close()

    # Calcular promedio por semáforo
    resultados = {}
    for tls_id, delays in delay_por_tls.items():
        if delays:
            promedio = sum(delays) / len(delays)
        else:
            promedio = None
        resultados[tls_id] = promedio

    return resultados
def correr_simulacion_limited(cfg_path, steps=500, salida="resultados/metrics_test.csv"):
    traci.start(["sumo-gui", "-c", cfg_path])

    semaforos = traci.trafficlight.getIDList()
    logger = MetricsLogger(semaforo_ids=semaforos)

    for step in range(steps):
        traci.simulationStep()
        logger.update(step)

    traci.close()
    logger.export_to_csv(salida)