import os
dirs_ = len([item for item in os.listdir("Semaforos") if os.path.isdir(os.path.join("Semaforos", item))])

for iter in range(1, dirs_+1):
    """os.makedirs(f"configs/Semaforos/iter_{iter}", exist_ok=True)"""
    semaforos = os.listdir(f"Semaforos/iter_{iter}")
    cantidad_semaforos = len(semaforos)
    print(f"Cantidad de semáforos en iteracion {iter}: {cantidad_semaforos}")