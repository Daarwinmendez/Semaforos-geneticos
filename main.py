import traci
#from utils.helpers import calcular_road_rage, contar_vehiculos
#from optimizador.cliente import ClienteSemaforo
'''from utils.helpers import contar_vehiculos

cantidad_carros = contar_vehiculos("mapa/osm.passenger.rou.xml")
cantidad_truck = contar_vehiculos("mapa/osm.truck.rou.xml")

print(f"Cantidad de Carros: {cantidad_carros}")
print(f"Cantidad de Camiones: {cantidad_truck}")
'''

traci.start(["sumo-gui", "-c", "mapa/osm.sumocfg"])

# Perform one simulation step to initialize the simulation
traci.simulationStep()

# Retrieve and print traffic light IDs and configurations
traffic_lights = traci.trafficlight.getIDList()
print(f"Traffic Lights: {traffic_lights}")

for tls_id in traffic_lights:
    configurations = traci.trafficlight.getCompleteRedYellowGreenDefinition(tls_id)
    print(f"Configurations for {tls_id}:")
    for config in configurations:
        print(config)

for step in range(1000):
    traci.simulationStep()
    for v in traci.vehicle.getIDList():
        print(f"{v}: {traci.vehicle.getPosition(v)}")

traci.close()
