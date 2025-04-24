import matplotlib.pyplot as plt
import os

def graficar_fitness_generaciones(fitness_por_generacion, nombre_img="fitness_evolucion.png"):
    """
    fitness_por_generacion: lista de dicts con keys 'max', 'mean', 'min' por generación
    """
    os.makedirs("resultados", exist_ok=True)
    generaciones = list(range(1, len(fitness_por_generacion) + 1))
    max_fit = [f["max"] for f in fitness_por_generacion]
    mean_fit = [f["mean"] for f in fitness_por_generacion]
    min_fit = [f["min"] for f in fitness_por_generacion]

    plt.figure(figsize=(8,5))
    plt.plot(generaciones, max_fit, label="Fitness Máximo")
    plt.plot(generaciones, mean_fit, label="Fitness Promedio")
    plt.plot(generaciones, min_fit, label="Fitness Mínimo")
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Evolución del Fitness por Generación")
    plt.legend()
    plt.tight_layout()
    path = os.path.join("resultados", nombre_img)
    plt.savefig(path)
    plt.close()
    print(f"Gráfica de fitness guardada en {path}")
