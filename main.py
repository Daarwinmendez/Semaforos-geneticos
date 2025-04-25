import traci
import json
import os
import random

'''iteration = 1
os.makedirs("configs/Semaforos/", exist_ok=True)
os.makedirs(f"configs/Semaforos/iter_{iteration}", exist_ok=True)

traci.start(["sumo", "-c", "Escenarios/1. Zona Universitaria (UASD)/osm.sumocfg"])
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

from genetico.generar_poblacion_inicial import generar_poblacion_inicial
from genetico.cromosoma import crossover_cromosomas, mutar_cromosoma
from genetico.seleccion_elite import seleccionar_elite
from genetico.benchmark import guardar_benchmark_generacion
from genetico.guardar_mejores import guardar_mejores_por_generacion
from genetico.graficar_fitness import graficar_fitness_generaciones
from genetico.aplicar_cromosoma import aplicar_cromosoma_a_jsons
from simulacion.controlador import correr_simulacion_limited
from utils.analisis_road_rage import analizar_road_rage
from utils.resumen_por_semaforo import resumen_por_semaforo
from genetico.guardar_resultados import guardar_resultados_generacion
from genetico.fitness import calcular_fitness_desde_csv
from utils.extractor import extraer_configuraciones_semaforos

def main():
    escenario_nombre = "2. Las Americas con Sabana y Venezuela"
    escenario_path = f"Escenarios/{escenario_nombre}/osm.sumocfg"
    base_semaforos = f"configs/Semaforos/base_{escenario_nombre.replace(' ', '_').replace('.', '')}"
    n_pobladores = 4
    n_generaciones = 2
    n_elite = 2
    prob_mutacion = 0.7

    # === EXTRAER BASE DINÁMICAMENTE ===
    if not (os.path.exists(base_semaforos) and len(os.listdir(base_semaforos)) > 0):
        print(f"[INFO] No se encontró configuración base para {escenario_nombre}, extrayendo...")
        extraer_configuraciones_semaforos(escenario_path, base_semaforos)
    else:
        print(f"[INFO] Configuración base para {escenario_nombre} ya existe, usando la existente.")

    poblacion = generar_poblacion_inicial(base_semaforos, n_pobladores=n_pobladores)
    benchmark_fitness = []
    mejores_cromosomas = []

    for gen in range(n_generaciones):
        print(f"\n=== GENERACIÓN {gen+1} ===")
        resultados = []
        for i, cromosoma in enumerate(poblacion):
            print(f"\nEvaluando cromosoma {i+1}/{n_pobladores}")

            carpeta_cromo_conf = f"configs/Semaforos/{escenario_nombre.replace(' ', '_').replace('.', '')}/gen{gen+1}_ind{i+1}"
            aplicar_cromosoma_a_jsons(cromosoma, carpeta_cromo_conf)

            carpeta_resultados = f"resultados/{escenario_nombre.replace(' ', '_').replace('.', '')}/gen{gen+1}_ind{i+1}"
            os.makedirs(carpeta_resultados, exist_ok=True)

            # ------------- dentro del for de evaluación -------------
            correr_simulacion_limited(
                cfg_path=escenario_path,
                steps=200,
                salida=os.path.join(carpeta_resultados, "metrics_test.csv"),
                carpeta_config=carpeta_cromo_conf,
                seed=random.randint(1, 10**6)   # ← NUEVO: cambia la semilla cada vez
            )
            analizar_road_rage(
                path_csv=os.path.join(carpeta_resultados, "metrics_test.csv"),
                salida_csv=os.path.join(carpeta_resultados, "road_rage_por_step.csv")
            )
            resumen_por_semaforo(
                path_csv=os.path.join(carpeta_resultados, "metrics_test.csv"),
                salida_csv=os.path.join(carpeta_resultados, "resumen_semaforos.csv")
            )
            fitness = calcular_fitness_desde_csv(os.path.join(carpeta_resultados, "road_rage_por_step.csv"))
            print(f"[INFO] Fitness cromosoma {i+1}: {fitness}")

            resultados.append({
                "indice": i,
                "cromosoma": cromosoma,
                "fitness": fitness,
                "carpeta_conf": carpeta_cromo_conf,
                "carpeta_resultados": carpeta_resultados
            })

        nombre_archivo = f"resultados_generacion_{gen+1}.json"
        guardar_resultados_generacion(resultados, nombre_archivo=nombre_archivo)

        # === ELITE Y EVOLUCIÓN ===
        elite = seleccionar_elite(f"resultados/{nombre_archivo}", n_elite=n_elite)
        elite_cromosomas = [e['cromosoma'] for e in elite]

        fitness_list = [r["fitness"] for r in resultados]
        benchmark_fitness.append({
            "generacion": gen+1,
            "max": max(fitness_list),
            "mean": sum(fitness_list)/len(fitness_list),
            "min": min(fitness_list)
        })
        mejores_cromosomas.append({
            "generacion": gen+1,
            "elite": elite
        })

        hijos = []
        while len(hijos) + len(elite_cromosomas) < n_pobladores:
            padres = random.sample(elite_cromosomas, 2)
            hijo = crossover_cromosomas(padres[0], padres[1])
            hijo_mutado = mutar_cromosoma(hijo, prob_mutacion=prob_mutacion)
            hijos.append(hijo_mutado)
        poblacion = elite_cromosomas + hijos

    guardar_benchmark_generacion(benchmark_fitness)
    guardar_mejores_por_generacion(mejores_cromosomas)
    graficar_fitness_generaciones(benchmark_fitness)

    # === SIMULACIÓN FINAL DEL MEJOR ===
    all_elite = []
    for gen_elite in mejores_cromosomas:
        all_elite.extend(gen_elite["elite"])
    mejor_global = max(all_elite, key=lambda x: x["fitness"])
    cromosoma_mejor = mejor_global["cromosoma"]

    carpeta_mejor_conf = f"configs/Semaforos/{escenario_nombre.replace(' ', '_').replace('.', '')}/mejor_global"
    carpeta_resultados_final = f"resultados/{escenario_nombre.replace(' ', '_').replace('.', '')}/mejor_global"
    aplicar_cromosoma_a_jsons(cromosoma_mejor, carpeta_mejor_conf)
    os.makedirs(carpeta_resultados_final, exist_ok=True)

    correr_simulacion_limited(
        cfg_path=escenario_path,
        steps=200,
        salida=os.path.join(carpeta_resultados_final, "metrics_test.csv"),
        carpeta_config=carpeta_mejor_conf
    )
    analizar_road_rage(
        path_csv=os.path.join(carpeta_resultados_final, "metrics_test.csv"),
        salida_csv=os.path.join(carpeta_resultados_final, "road_rage_por_step.csv")
    )
    resumen_por_semaforo(
        path_csv=os.path.join(carpeta_resultados_final, "metrics_test.csv"),
        salida_csv=os.path.join(carpeta_resultados_final, "resumen_semaforos.csv")
    )
    guardar_benchmark_generacion(benchmark_fitness)

if __name__ == "__main__":
    main()