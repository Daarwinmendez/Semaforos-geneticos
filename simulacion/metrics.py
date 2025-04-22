import traci
import math

def calcular_retraso_vehiculo(veh_id, semaforo_pos, tolerancia=5.0):
    """
    Calcula el retraso que tuvo un vehículo en llegar al semáforo.
    """
    pos_veh = traci.vehicle.getPosition(veh_id)
    distancia = math.dist(pos_veh, semaforo_pos)

    # Si está lo suficientemente cerca, lo consideramos "llegando"
    if distancia <= tolerancia:
        arrival_real = traci.simulation.getTime()
        depart = traci.vehicle.getDeparture(veh_id)
        velocidad = traci.vehicle.getAllowedSpeed(veh_id)

        # Estimación de la distancia recorrida
        distancia_recorrida = traci.vehicle.getDistance(veh_id)

        arrival_esperado = depart + (distancia_recorrida / velocidad)
        delay = arrival_real - arrival_esperado

        return max(0, delay)  # Siempre >= 0
    return None
