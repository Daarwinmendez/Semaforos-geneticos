# Funciones de ayuda, lectura/escritura XML, etc.
import xml.etree.ElementTree as ET



def contar_vehiculos(archivo_xml, etiqueta='vehicle'):
    """
    Cuenta el número de vehículos en un archivo XML.

    Args:
        archivo_xml (str): Ruta al archivo XML.
        etiqueta (str): Etiqueta XML que representa un vehículo. Por defecto es 'vehicle'.

    Returns:
        int: Número de vehículos que cumplen con el criterio de la etiqueta.
    """
    try:
        tree = ET.parse(archivo_xml)
        root = tree.getroot()
        ids = set()
        for trip in root.findall(etiqueta):
            veh_id = trip.get('id')
            if veh_id not in ids:
                ids.add(veh_id)
            
        return len(ids)
    except ET.ParseError as e:
        print(f"Error al analizar el archivo XML: {e}")
        return 0
    except FileNotFoundError:
        print(f"El archivo {archivo_xml} no fue encontrado.")
        return 0
    

def calcular_road_rage(traci, rage_dict=None, epsilon=0.1):
    if rage_dict is None:
        rage_dict = {}

    for veh_id in traci.vehicle.getIDList():
        speed = traci.vehicle.getSpeed(veh_id)

        if veh_id not in rage_dict:
            rage_dict[veh_id] = 0

        if speed < epsilon:
            rage_dict[veh_id] += 1

    return rage_dict

def contar_semaforos(archivo_xml, etiqueta='tlLogic'):
    """
    Cuenta el número de semáforos en un archivo XML.

    Args:
        archivo_xml (str): Ruta al archivo XML.
        etiqueta (str): Etiqueta XML que representa un semáforo. Por defecto es 'tlLogic'.

    Returns:
        int: Número de semáforos que cumplen con el criterio de la etiqueta.
    """
    try:
        tree = ET.parse(archivo_xml)
        root = tree.getroot()
        semaforos = root.findall(etiqueta)
        return len(semaforos)
    except ET.ParseError as e:
        print(f"Error al analizar el archivo XML: {e}")
        return 0
    except FileNotFoundError:
        print(f"El archivo {archivo_xml} no fue encontrado.")
        return 0
    
count_sem_map1 = contar_semaforos(r'C:\Users\micha\OneDrive\Documentos\Cosas-de-la-Uni\Tareas-y-Trabajos-de-IA-Distribuida\-Proyectos-de-DAI\Proyecto Final\Semaforos-geneticos\Escenarios\1. Zona Universitaria (UASD)\osm.net.xml')
count_sem_map2 = contar_semaforos(r'C:\Users\micha\OneDrive\Documentos\Cosas-de-la-Uni\Tareas-y-Trabajos-de-IA-Distribuida\-Proyectos-de-DAI\Proyecto Final\Semaforos-geneticos\Escenarios\2. Las Americas con Sabana y Venezuela\osm.net.xml')
count_sem_map3 = contar_semaforos(r'C:\Users\micha\OneDrive\Documentos\Cosas-de-la-Uni\Tareas-y-Trabajos-de-IA-Distribuida\-Proyectos-de-DAI\Proyecto Final\Semaforos-geneticos\Escenarios\3. Zona Megacentro (Av. San Vicente P.)\osm.net.xml')
count_sem_map4 = contar_semaforos(r'C:\Users\micha\OneDrive\Documentos\Cosas-de-la-Uni\Tareas-y-Trabajos-de-IA-Distribuida\-Proyectos-de-DAI\Proyecto Final\Semaforos-geneticos\Escenarios\4. Av. Jhon F. Kennedy con Abraham Lincoln\osm.net.xml')
count_sem_map5 = contar_semaforos(r'C:\Users\micha\OneDrive\Documentos\Cosas-de-la-Uni\Tareas-y-Trabajos-de-IA-Distribuida\-Proyectos-de-DAI\Proyecto Final\Semaforos-geneticos\Escenarios\5. Av. 27 de Febrero con Maximo G\osm.net.xml')


print(f"El número de semáforos del escenario 1 es: {count_sem_map1}")
print(f"El número de semáforos del escenario 2 es: {count_sem_map2}")
print(f"El número de semáforos del escenario 3 es: {count_sem_map3}")
print(f"El número de semáforos del escenario 4 es: {count_sem_map4}")
print(f"El número de semáforos del escenario 5 es: {count_sem_map5}")