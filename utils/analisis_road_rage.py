import pandas as pd
import os

def analizar_road_rage(path_csv="resultados/metrics_test.csv", salida_csv="resultados/road_rage_por_step.csv"):
    # Cargar métricas por step
    df = pd.read_csv(path_csv)

    # Separar vehículos y semáforos
    veh_df = df[df["tipo"] == "vehiculo"].copy()
    sem_df = df[df["tipo"] == "semaforo"].copy()

    # Forzar a numérico para evitar errores al hacer mean()
    for col in ["delay", "waiting_time", "stops"]:
        veh_df[col] = pd.to_numeric(veh_df[col], errors="coerce")

    # Agrupar métricas de vehículos por step
    veh_agg = veh_df.groupby("step").agg({
        "delay": "mean",
        "waiting_time": "mean",
        "stops": "mean"
    }).reset_index()

    # Agrupar cola promedio por step desde los semáforos
    queue_agg = sem_df.groupby("step")["queue_length"].mean().reset_index()

    # Unir ambas métricas por step
    merged = pd.merge(veh_agg, queue_agg, on="step", how="left")

    # Calcular road rage (ajustado y normalizado)
    merged["road_rage"] = (
        0.4 * (merged["delay"] / 10) +
        0.2 * (merged["stops"] / 5) +
        0.2 * (merged["waiting_time"] / 10) +
        0.2 * (merged["queue_length"] / 10)
    ).clip(upper=1.0)  # limitar a 1.0 como máximo

    # Exportar resultados
    os.makedirs(os.path.dirname(salida_csv), exist_ok=True)
    merged.to_csv(salida_csv, index=False)

    # Imprimir resumen
    print(merged.head())
    print("\nPromedio de Road Rage total:", merged["road_rage"].mean())