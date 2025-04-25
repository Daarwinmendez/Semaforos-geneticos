import os, random
from pathlib import Path
import traci

# módulos del proyecto 
from genetico.generar_poblacion_inicial import generar_poblacion_inicial
from genetico.cromosoma import crossover_cromosomas, mutar_cromosoma
from genetico.aplicar_cromosoma import aplicar_cromosoma_a_jsons
from genetico.seleccion_prob import seleccionar_padres_probabilidad
from genetico.fitness import calcular_fitness_desde_csv
from genetico.guardar_resultados import guardar_resultados_generacion
from genetico.benchmark import guardar_benchmark_generacion
from genetico.guardar_mejores import guardar_mejores_por_generacion
from genetico.graficar_fitness  import graficar_fitness_generaciones
from simulacion.controlador import correr_simulacion_limited
from utils.analisis_road_rage import analizar_road_rage
from utils.resumen_por_semaforo import resumen_por_semaforo
from utils.extractor import extraer_configuraciones_semaforos

def general(escenario_nombre) -> None:
    # parámetros generales
    escenario_id     = escenario_nombre.replace(" ", "_").replace(".", "")
    escenario_path   = f"Escenarios/{escenario_nombre}/osm.sumocfg"

    base_semaforos   = f"configs/Semaforos/base_{escenario_id}"
    ruta_escenario   = Path("resultados") / escenario_id
    ruta_escenario.mkdir(parents=True, exist_ok=True)

    n_pobladores   = 10
    n_generaciones = 8
    selection_rate = 0.5
    prob_mutacion  = 0.45
    sim_steps      = 800

    # extraer confs base si no existen 
    if not (os.path.exists(base_semaforos) and os.listdir(base_semaforos)):
        print("[INFO] Extrayendo configuraciones base…")
        extraer_configuraciones_semaforos(escenario_path, base_semaforos)

    # población inicial
    poblacion         = generar_poblacion_inicial(base_semaforos, n_pobladores)
    benchmark_fitness = []
    mejores_generales = []

    # bucle de generaciones
    for gen in range(1, n_generaciones + 1):
        print(f"\n=== GENERACIÓN {gen} ===")
        gen_dir    = ruta_escenario / f"gen{gen}"
        gen_dir.mkdir(parents=True, exist_ok=True)
        resultados = []

        for idx, cromosoma in enumerate(poblacion, start=1):
            print(f"\nEvaluando cromosoma {idx}/{n_pobladores}")

            # carpeta de configuración y carpeta de resultados por individuo
            carpeta_conf = f"configs/Semaforos/{escenario_id}/gen{gen}/ind{idx}"
            aplicar_cromosoma_a_jsons(cromosoma, carpeta_conf)

            ind_dir = gen_dir / f"ind{idx}"
            ind_dir.mkdir(parents=True, exist_ok=True)

            metrics_csv = ind_dir / "metrics.csv"
            rage_csv    = ind_dir / "rage.csv"
            sem_csv     = ind_dir / "semaforos.csv"

            # simulación
            correr_simulacion_limited(
                cfg_path=escenario_path,
                steps=sim_steps,
                salida=str(metrics_csv),
                carpeta_config=carpeta_conf,
                seed=random.randint(1, 10**6)
            )

            analizar_road_rage(str(metrics_csv), str(rage_csv))
            resumen_por_semaforo(str(metrics_csv), str(sem_csv))

            fitness_val = calcular_fitness_desde_csv(str(rage_csv))
            print(f"[INFO] Fitness cromosoma {idx}: {fitness_val:.6f}")

            resultados.append({
                "indice"   : idx,
                "cromosoma": cromosoma,
                "fitness"  : fitness_val,
                "files"    : {
                    "metrics" : str(metrics_csv),
                    "rage"    : str(rage_csv),
                    "semaforo": str(sem_csv)
                }
            })

        # persistir resultados de la generación 
        nombre_json = gen_dir / f"resultados_generacion_{gen}.json"
        guardar_resultados_generacion(resultados, nombre_archivo=str(nombre_json))

        fitness_vals = [r["fitness"] for r in resultados]
        benchmark_fitness.append({
            "generacion": gen,
            "max" : max(fitness_vals),
            "mean": sum(fitness_vals) / len(fitness_vals),
            "min" : min(fitness_vals)
        })

        mejor_gen = max(resultados, key=lambda r: r["fitness"])
        mejores_generales.append({"generacion": gen, "mejor": mejor_gen})

        # selección, cruce y mutación
        padres_pool = seleccionar_padres_probabilidad(
            path_resultados_json=str(nombre_json),
            k=int(n_pobladores * selection_rate)
        )

        hijos = []
        while len(hijos) + len(padres_pool) < n_pobladores:
            p1, p2 = random.sample(padres_pool, 2)
            hijo   = crossover_cromosomas(p1, p2)
            hijo   = mutar_cromosoma(hijo, prob_mutacion=prob_mutacion)
            hijos.append(hijo)

        poblacion = padres_pool + hijos

    # reportes globales
    guardar_benchmark_generacion(
        benchmark_fitness,
        ruta_escenario,              
        "benchmark_generaciones.csv"
    )
    guardar_mejores_por_generacion(
        mejores_generales,
        ruta_escenario,
        "mejores_por_generacion.json"
    )
    graficar_fitness_generaciones(
        benchmark_fitness,
        nombre_img=str(ruta_escenario / "fitness_evolucion.png")
    )

    # simulación final del mejor global
    mejor_global  = max((g["mejor"] for g in mejores_generales), key=lambda r: r["fitness"])
    cromosoma_top = mejor_global["cromosoma"]

    carpeta_top_conf = f"configs/Semaforos/{escenario_id}/mejor_global"
    aplicar_cromosoma_a_jsons(cromosoma_top, carpeta_top_conf)

    top_dir     = ruta_escenario / "mejor_global"
    top_dir.mkdir(parents=True, exist_ok=True)
    metrics_top = top_dir / "metrics.csv"
    rage_top    = top_dir / "rage.csv"
    sem_top     = top_dir / "semaforos.csv"

    correr_simulacion_limited(
        cfg_path=escenario_path,
        steps=sim_steps,
        salida=str(metrics_top),
        carpeta_config=carpeta_top_conf
    )
    analizar_road_rage(str(metrics_top), str(rage_top))
    resumen_por_semaforo(str(metrics_top), str(sem_top))

# al descubrir escenarios 
def escenarios_validos(root="Escenarios"):
    for nombre in os.listdir(root):
        ruta = Path(root) / nombre
        if ruta.is_dir() and any(ruta.glob("*.sumocfg")):
            yield nombre

if __name__ == "__main__":
    for escenario in escenarios_validos():
        print(f"\n=== ESCENARIO: {escenario} ===")
        general(escenario)
        print(f"[OK] Simulación y análisis de {escenario} finalizados.")
        print("───────────────────────────────────────────────────────────────")
