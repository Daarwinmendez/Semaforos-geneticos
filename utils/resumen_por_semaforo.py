import os
import pandas as pd
from pathlib import Path

def resumen_por_semaforo(path_csv: str, salida_csv: str) -> None:
    """
    Crea dos archivos en la misma carpeta de `salida_csv`:
      • resumen bruto   → <salida_csv>
      • resumen _norm   → <salida_csv_base>_norm.csv
    """
    df = pd.read_csv(path_csv)

    veh_df = df[df["tipo"] == "vehiculo"].copy()
    sem_df = df[df["tipo"] == "semaforo"].copy()

    for col in ["delay", "waiting_time", "stops"]:
        veh_df[col] = pd.to_numeric(veh_df[col], errors="coerce")
    sem_df["queue_length"] = pd.to_numeric(sem_df["queue_length"], errors="coerce")

    # ―― métricas de vehículos ――
    veh_metrics = (
        veh_df
        .groupby("semaforo_id")
        .agg({
            "delay"        : "mean",
            "waiting_time" : "mean",
            "stops"        : "mean",
            "veh_id"       : "count"
        })
        .rename(columns={"veh_id": "flujo_vehicular"})
        .reset_index()
    )

    pasos_sim = df["step"].max() + 1
    veh_metrics["flujo_por_segundo"] = veh_metrics["flujo_vehicular"] / pasos_sim

    # ―― colas ――
    queue_avg = (
        sem_df
        .groupby("semaforo_id")["queue_length"]
        .mean()
        .reset_index()
    )

    resumen = pd.merge(veh_metrics, queue_avg, on="semaforo_id", how="left")

    # guardar resumen bruto
    Path(os.path.dirname(salida_csv)).mkdir(parents=True, exist_ok=True)
    resumen.to_csv(salida_csv, index=False)

    # ―― normalización ――
    normalizado = resumen.copy()
    cols_norm = ["delay", "waiting_time", "stops",
                 "flujo_vehicular", "flujo_por_segundo", "queue_length"]

    for col in cols_norm:
        max_v, min_v = normalizado[col].max(), normalizado[col].min()
        normalizado[f"{col}_norm"] = 0.0 if max_v == min_v else (
            (normalizado[col] - min_v) / (max_v - min_v)
        )

    normalizado["road_rage"] = (
        0.4 * (resumen["delay"]        / 10) +
        0.2 * (resumen["stops"]        / 5 ) +
        0.2 * (resumen["waiting_time"] / 10)
    ).clip(upper=1.0)

    base, _ = os.path.splitext(salida_csv)
    norm_path = f"{base}_norm.csv"
    normalizado.to_csv(norm_path, index=False)

    print(f"[OK] Resumen guardado en: {salida_csv}")
    print(f"[OK] Resumen normalizado en: {norm_path}")
