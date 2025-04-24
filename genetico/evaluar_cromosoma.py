from simulacion.controlador import correr_simulacion_limited
from utils.analisis_road_rage import analizar_road_rage
from utils.resumen_por_semaforo import resumen_por_semaforo
import os

from genetico.fitness import calcular_fitness_desde_csv

def evaluar_cromosoma(cfg_path, carpeta_semaforos, cromosoma, steps=200, carpeta_resultados="resultados/tmp_eval"):
    from genetico.aplicar_cromosoma import aplicar_cromosoma_a_jsons

    aplicar_cromosoma_a_jsons(cromosoma, carpeta_semaforos)
    correr_simulacion_limited(
        cfg_path=cfg_path, 
        steps=steps, 
        salida=os.path.join(carpeta_resultados, "metrics_test.csv"),
        carpeta_config=carpeta_semaforos
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
    return fitness