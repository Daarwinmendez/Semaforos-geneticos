import pandas as pd
import os

def resumen_por_semaforo(path_csv="resultados/metrics_test.csv", salida_csv="resultados/resumen_semaforos.csv"):
    df = pd.read_csv(path_csv)

    # Filtrar datos
    veh_df = df[df["tipo"] == "vehiculo"].copy()
    sem_df = df[df["tipo"] == "semaforo"].copy()

    # Asegurar numéricos en las columnas clave
    for col in ["delay", "waiting_time", "stops"]:
        veh_df[col] = pd.to_numeric(veh_df[col], errors="coerce")
    sem_df["queue_length"] = pd.to_numeric(sem_df["queue_length"], errors="coerce")

    # Agrupar métricas de vehículos por semáforo_id
    veh_metrics = veh_df.groupby("semaforo_id").agg({
        "delay": "mean",
        "waiting_time": "mean",
        "stops": "mean",
        "veh_id": "count"
    }).rename(columns={"veh_id": "flujo_vehicular"}).reset_index()

    # Flujo por segundo
    pasos_simulados = df["step"].max() + 1
    veh_metrics["flujo_por_segundo"] = veh_metrics["flujo_vehicular"] / pasos_simulados

    # Agrupar promedio de cola por semáforo
    queue_avg = sem_df.groupby("semaforo_id")["queue_length"].mean().reset_index()

    # Unir todo por semáforo_id
    resumen = pd.merge(veh_metrics, queue_avg, on="semaforo_id", how="left")

    # Guardar archivo sin normalizar
    os.makedirs(os.path.dirname(salida_csv), exist_ok=True)
    resumen.to_csv(salida_csv, index=False)

    # Normalizar las columnas clave
    normalizado = resumen.copy()
    columnas_a_normalizar = ["delay", "waiting_time", "stops", "flujo_vehicular", "flujo_por_segundo", "queue_length"]
    for col in columnas_a_normalizar:
        max_val = normalizado[col].max()
        min_val = normalizado[col].min()
        if max_val != min_val:
            normalizado[col + "_norm"] = (normalizado[col] - min_val) / (max_val - min_val)
        else:
            normalizado[col + "_norm"] = 0.0

    # Normalizar road_rage como ya estaba definido
    normalizado["road_rage"] = (
        0.4 * (resumen["delay"] / 10) +
        0.2 * (resumen["stops"] / 5) +
        0.2 * (resumen["waiting_time"] / 10)
    ).clip(upper=1.0)

    # Guardar archivo normalizado
    normalizado.to_csv("resultados/resumen_semaforos_normalizado.csv", index=False)

    print("Resumen por semáforo guardado en:", salida_csv)
    print("Resumen normalizado guardado en: resultados/resumen_semaforos_normalizado.csv")
    print(normalizado.head())