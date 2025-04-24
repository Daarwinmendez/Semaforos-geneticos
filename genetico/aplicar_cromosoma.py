import os
import json

def aplicar_cromosoma_a_jsons(cromosoma, carpeta_salida):
    """
    Guarda la configuración del cromosoma (dict) en archivos individuales en la carpeta_salida.
    Cada archivo representa un semáforo con su configuración.
    """
    os.makedirs(carpeta_salida, exist_ok=True)

    for s_id, config in cromosoma.items():
        archivo_salida = os.path.join(carpeta_salida, f"{s_id}.json")
        with open(archivo_salida, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        print(f"[✔] Guardado {archivo_salida} con offset={config.get('offset')} y {len(config.get('phases', []))} fases.")

    print(f"[OK] Se aplicaron y guardaron {len(cromosoma)} configuraciones de semáforos en: {carpeta_salida}\n")
