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

    
