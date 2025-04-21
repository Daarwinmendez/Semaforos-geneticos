import traci

class ClienteSemaforo:
    def __init__(self, id_semaforo, configuracion):
        self.id = id_semaforo
        self.configuracion = configuracion  # lista de fases: [{"state": "GrGr", "duration": 30}, ...]
        self.fitness = None

    def aplicar_configuracion(self, program_id="optimo"):
        """
        Aplica la configuración actual al semáforo usando TraCI.
        """
        traci.trafficlight.setProgramLogic(self.id, traci.trafficlight.Logic(
            programID=program_id,
            type=0,  # static
            currentPhaseIndex=0,
            phases=[
                traci.trafficlight.Phase(phase["duration"], phase["state"])
                for phase in self.configuracion
            ]
        ))

    def evaluar(self, metricas_globales):
        """
        Asigna un fitness a este semáforo con base en las métricas globales (como road rage).
        """
        self.fitness = metricas_globales.get(self.id, 9999)

    def __repr__(self):
        return f"<ClienteSemaforo id={self.id} fitness={self.fitness}>"
