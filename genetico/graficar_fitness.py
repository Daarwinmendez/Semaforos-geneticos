import matplotlib.pyplot as plt
from pathlib import Path

def graficar_fitness_generaciones(
        fitness_por_generacion,
        nombre_img: str = "fitness_evolucion.png"
    ) -> None:
    """
    Dibuja y guarda la curva de fitness.

    • Si `nombre_img` contiene carpeta, se respeta tal cual.
    • Si es solo un nombre, se guarda en 'resultados/' (modo legacy).
    """
    # preparar ruta
    if "/" in nombre_img or "\\" in nombre_img:   
        path = Path(nombre_img)
    else:                                        
        path = Path("resultados") / nombre_img

    path.parent.mkdir(parents=True, exist_ok=True)

    # preparar datos 
    generaciones = list(range(1, len(fitness_por_generacion) + 1))
    max_fit  = [f["max"]  for f in fitness_por_generacion]
    mean_fit = [f["mean"] for f in fitness_por_generacion]
    min_fit  = [f["min"]  for f in fitness_por_generacion]

    plt.figure(figsize=(8, 5))
    plt.plot(generaciones, max_fit,  label="Fitness Máximo")
    plt.plot(generaciones, mean_fit, label="Fitness Promedio")
    plt.plot(generaciones, min_fit,  label="Fitness Mínimo")
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Evolución del Fitness por Generación")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    print(f"[OK] Gráfica de fitness guardada en {path}")
