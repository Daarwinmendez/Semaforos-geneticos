import traci
import pandas as pd
import math

class MetricsLogger:
    def __init__(self, semaforo_ids, vehiculos_esperados=None):
        self.semaforo_ids = semaforo_ids
        self.vehiculos_esperados = vehiculos_esperados or {}
        self.depart_times = {}  # para generar depart_time si no se da
        self.records = []

    def get_vehicle_delay(self, veh_id):
        current_time = traci.simulation.getTime()
        if veh_id not in self.depart_times:
            self.depart_times[veh_id] = current_time
        depart_time = self.depart_times[veh_id]

        # estimar distancia recorrida desde que entró (opcional)
        distancia = traci.vehicle.getDistance(veh_id)
        velocidad = traci.vehicle.getAllowedSpeed(veh_id)
        if velocidad > 0:
            expected_time = depart_time + (distancia / velocidad)
            return max(0, current_time - expected_time)
        return 0

    def get_waiting_time(self, veh_id):
        return traci.vehicle.getWaitingTime(veh_id)

    def get_vehicle_stops(self, veh_id):
        return traci.vehicle.getStops(veh_id)

    def get_position(self, veh_id):
        return traci.vehicle.getPosition(veh_id)

    def get_speed(self, veh_id):
        return traci.vehicle.getSpeed(veh_id)

    def get_queue_length(self, semaforo_id):
        lanes = traci.trafficlight.getControlledLanes(semaforo_id)
        return sum(traci.lane.getLastStepHaltingNumber(lane) for lane in lanes)

    def update(self, step):
        for veh_id in traci.vehicle.getIDList():
            pos = self.get_position(veh_id)
            speed = self.get_speed(veh_id)
            stops = self.get_vehicle_stops(veh_id)
            delay = self.get_vehicle_delay(veh_id)
            waiting = self.get_waiting_time(veh_id)

            self.records.append({
                "tipo": "vehiculo",
                "step": step,
                "veh_id": veh_id,
                "delay": delay,
                "waiting_time": waiting,
                "stops": stops,
                "pos_x": pos[0],
                "pos_y": pos[1],
                "speed": speed
            })

        for semaforo_id in self.semaforo_ids:
            queue = self.get_queue_length(semaforo_id)
            self.records.append({
                "tipo": "semaforo",
                "step": step,
                "semaforo_id": semaforo_id,
                "queue_length": queue
            })

    def to_dataframe(self):
        return pd.DataFrame(self.records)

    def export_to_csv(self, path):
        df = self.to_dataframe()
        df.to_csv(path, index=False)

    def clear(self):
        self.records = []
        self.depart_times = {}
