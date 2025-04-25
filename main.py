import traci
import json
import os
import random

from genetico.generar_poblacion_inicial import generar_poblacion_inicial
from genetico.cromosoma import crossover_cromosomas, mutar_cromosoma
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
from genetico.seleccion_prob import seleccionar_padres_probabilidad   # ← NUEVO

def main() -> None:
    # ---------- parámetros ----------
    escenario_nombre  = "2. Las Americas con Sabana y Venezuela"
    escenario_path    = f"Escenarios/{escenario_nombre}/osm.sumocfg"
    base_semaforos    = f"configs/Semaforos/base_{escenario_nombre.replace(' ', '_').replace('.', '')}"

    n_pobladores      = 8
    n_generaciones    = 2
    selection_rate    = 0.5          # ← % de la población que pasa al “pool” de padres
    prob_mutacion     = 0.7
    sim_steps         = 200

    # ---------- extraer configuraciones base ----------
    if not (os.path.exists(base_semaforos) and os.listdir(base_semaforos)):
        print(f"[INFO] No se encontró configuración base para {escenario_nombre}, extrayendo…")
        extraer_configuraciones_semaforos(escenario_path, base_semaforos)
    else:
        print(f"[INFO] Configuración base encontrada. Usando {base_semaforos}")

    # ---------- población inicial ----------
    poblacion          = generar_poblacion_inicial(base_semaforos, n_pobladores=n_pobladores)
    benchmark_fitness  = []
    mejores_generales  = []      # para guardar el mejor de cada generación

    # ---------- bucle de generaciones ----------
    for gen in range(1, n_generaciones + 1):
        print(f"\n=== GENERACIÓN {gen} ===")
        resultados = []

        # --- evaluar cada cromosoma ---
        for idx, cromosoma in enumerate(poblacion, start=1):
            print(f"\nEvaluando cromosoma {idx}/{n_pobladores}")

            carpeta_conf = (
                f"configs/Semaforos/{escenario_nombre.replace(' ', '_').replace('.', '')}"
                f"/gen{gen}_ind{idx}"
            )
            aplicar_cromosoma_a_jsons(cromosoma, carpeta_conf)

            carpeta_res  = (
                f"resultados/{escenario_nombre.replace(' ', '_').replace('.', '')}"
                f"/gen{gen}_ind{idx}"
            )
            os.makedirs(carpeta_res, exist_ok=True)

            correr_simulacion_limited(
                cfg_path=escenario_path,
                steps=sim_steps,
                salida=os.path.join(carpeta_res, "metrics_test.csv"),
                carpeta_config=carpeta_conf,
                seed=random.randint(1, 10**6)          # semilla aleatoria
            )
            analizar_road_rage(
                path_csv=os.path.join(carpeta_res, "metrics_test.csv"),
                salida_csv=os.path.join(carpeta_res, "road_rage_por_step.csv")
            )
            resumen_por_semaforo(
                path_csv=os.path.join(carpeta_res, "metrics_test.csv"),
                salida_csv=os.path.join(carpeta_res, "resumen_semaforos.csv")
            )

            fitness_val = calcular_fitness_desde_csv(
                os.path.join(carpeta_res, "road_rage_por_step.csv")
            )
            print(f"[INFO] Fitness cromosoma {idx}: {fitness_val:.6f}")

            resultados.append({
                "indice": idx,
                "cromosoma": cromosoma,
                "fitness": fitness_val,
                "carpeta_conf": carpeta_conf,
                "carpeta_resultados": carpeta_res
            })

        # --- guardar tabla cruda de la generación ---
        nombre_json = f"resultados_generacion_{gen}.json"
        guardar_resultados_generacion(resultados, nombre_archivo=nombre_json)

        # --- estadísticas para el benchmark ---
        fitness_list = [r["fitness"] for r in resultados]
        benchmark_fitness.append({
            "generacion": gen,
            "max":   max(fitness_list),
            "mean":  sum(fitness_list) / len(fitness_list),
            "min":   min(fitness_list)
        })

        # --- mejor de la generación (para informe final) ---
        mejor_gen = max(resultados, key=lambda r: r["fitness"])
        mejores_generales.append({"generacion": gen, "mejor": mejor_gen})

        # --- SELECCIÓN PROBABILÍSTICA DE PADRES ---
        padres_pool = seleccionar_padres_probabilidad(
            path_resultados_json=f"resultados/{nombre_json}",
            k=int(n_pobladores * selection_rate)
        )

        # --- CRUCE + MUTACIÓN para completar población ---
        hijos = []
        while len(hijos) + len(padres_pool) < n_pobladores:
            p1, p2 = random.sample(padres_pool, 2)
            hijo   = crossover_cromosomas(p1, p2)
            hijo   = mutar_cromosoma(hijo, prob_mutacion=prob_mutacion)
            hijos.append(hijo)

        poblacion = padres_pool + hijos      # nueva población

    # ---------- post-proceso ----------
    guardar_benchmark_generacion(benchmark_fitness)
    guardar_mejores_por_generacion(mejores_generales)
    graficar_fitness_generaciones(benchmark_fitness)

    # ---------- simulación final del mejor global ----------
    mejor_global = max(
        (g["mejor"] for g in mejores_generales),
        key=lambda r: r["fitness"]
    )
    cromosoma_top = mejor_global["cromosoma"]

    carpeta_mejor_conf = (
        f"configs/Semaforos/{escenario_nombre.replace(' ', '_').replace('.', '')}/mejor_global"
    )
    carpeta_res_final  = (
        f"resultados/{escenario_nombre.replace(' ', '_').replace('.', '')}/mejor_global"
    )
    aplicar_cromosoma_a_jsons(cromosoma_top, carpeta_mejor_conf)
    os.makedirs(carpeta_res_final, exist_ok=True)

    correr_simulacion_limited(
        cfg_path=escenario_path,
        steps=sim_steps,
        salida=os.path.join(carpeta_res_final, "metrics_test.csv"),
        carpeta_config=carpeta_mejor_conf
    )
    analizar_road_rage(
        path_csv=os.path.join(carpeta_res_final, "metrics_test.csv"),
        salida_csv=os.path.join(carpeta_res_final, "road_rage_por_step.csv")
    )
    resumen_por_semaforo(
        path_csv=os.path.join(carpeta_res_final, "metrics_test.csv"),
        salida_csv=os.path.join(carpeta_res_final, "resumen_semaforos.csv")
    )
    guardar_benchmark_generacion(benchmark_fitness)

if __name__ == "__main__":
    main()
