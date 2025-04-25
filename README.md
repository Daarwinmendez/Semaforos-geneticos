# 🚦 Proyecto Semáforos Genéticos – Optimización de Tráfico Urbano con Algoritmos Evolutivos 🚦

> **Optimización avanzada de intersecciones urbanas dominicanas mediante algoritmos genéticos, simulación distribuida y análisis automatizado de métricas de tráfico.**

---

## ✨ Motivación

En el contexto de las grandes ciudades, los tapones y la mala sincronización de semáforos representan uno de los principales causantes de estrés, pérdida de tiempo y emisiones contaminantes. **Este proyecto nace para atacar ese problema usando inteligencia artificial aplicada y simulación realista**.

La meta es desarrollar una solución capaz de aprender, comparar y evolucionar las mejores configuraciones de semáforos para reducir el “road rage” (estrés vial) y optimizar el flujo vehicular en las intersecciones más críticas de Santo Domingo.

---

## 🚦 ¿Qué hace este proyecto?

- Simula distintos escenarios reales de tráfico dominicano usando [SUMO](https://www.eclipse.org/sumo/).
- Aplica **algoritmos genéticos** para evolucionar la programación de semáforos (fases, tiempos y offsets).
- Evalúa el desempeño de cada configuración a través de una **métrica compuesta (“road rage”)** que refleja el nivel de congestión y eficiencia.
- Automatiza todo el ciclo: generación, simulación, evaluación, selección, cruzamiento, mutación, y análisis visual de resultados.
- Almacena todos los outputs de forma ordenada, auditando el desempeño de cada individuo (configuración) y generación.

---

## 🧬 Pipeline Evolutivo Completo

1. **Inicialización:**  
   Se genera una población de cromosomas, donde cada uno representa una posible configuración de semáforos en un escenario dado.

2. **Simulación:**  
   Cada cromosoma es simulado en SUMO. Se registran métricas detalladas por cada paso: delay, stops, colas, waiting time y más.

3. **Cálculo de “Road Rage”:**  
   Se calcula un índice compuesto (0 a 1) combinando las métricas de tráfico clave.  
   - 0: Tráfico ideal, sin tapón  
   - 1: Congestión total  
   **El objetivo es minimizar este valor.**

4. **Cálculo del Fitness:**  
   fitness = 1 - promedio_road_rage

   Así, un fitness más alto significa un mejor desempeño de la configuración de semáforos.

5. **Selección:**  
Se seleccionan los padres para la siguiente generación usando selección por ruleta (probabilidad proporcional al fitness).

6. **Crossover y Mutación:**  
Los padres se cruzan y mutan para producir hijos con nuevas configuraciones.

7. **Evolución:**  
El proceso se repite por varias generaciones, guardando siempre los resultados y las mejores configuraciones.

8. **Análisis y Visualización:**  
Se generan reportes automáticos (CSV, JSON, gráficos) para analizar la evolución del fitness y el impacto de las decisiones genéticas.

---

## 📊 Definición de Road Rage y Métricas

El “road rage” se define como una **métrica global de calidad de tráfico**, calculada como una combinación ponderada y normalizada de:
- **Retraso (delay)**
- **Número de stops**
- **Tiempo de espera**
- **Cola promedio (queue length)**

La fórmula es:
```python
road_rage = 0.4*(delay/10) + 0.2*(stops/5) + 0.2*(waiting_time/10) + 0.2*(queue_length/10)
road_rage = min(road_rage, 1.0)

```

* Interpretación:

- 0.0 – 0.2: Tráfico ideal, sincronización óptima.

- 0.2 – 0.5: Flujo aceptable, niveles normales para hora no pico.

- 0.5 – 1.0: Congestión severa, semáforo mal configurado o tapón crónico.

---

## 🤖 Características Técnicas

* **Automatización multi-escenario:**
  El script principal detecta todos los escenarios disponibles y corre el pipeline completo para cada uno, sin intervención manual.

* **Resultados ordenados y trazables:**
  Todos los outputs (CSV, gráficos, resúmenes, configuraciones) se guardan de forma jerárquica por escenario, generación e individuo.

* **Soporte robusto a rutas largas y sistemas Windows:**
  Manejo automático de rutas y creación de carpetas intermedias, evitando errores comunes de “filename too long”.

* **Compatibilidad avanzada:**
  Funciones compatibles con diversas versiones de pandas y matplotlib.

* **Escalable:**
  Fácilmente adaptable a más generaciones, individuos, o escenarios nuevos.

---

## ⚡ ¿Cómo ejecutar el proyecto?

1. **Prepara tus escenarios** en la carpeta Escenarios/ (cada uno con su archivo .sumocfg y archivos de red correspondientes).

2. Instala los requisitos (Python 3.8+, SUMO, pandas, matplotlib, etc).

3. Ejecuta el pipeline completo:

```python 

main.py

```
¡Listo! El sistema analizará cada escenario y dejará los resultados bien organizados y listos para análisis.

---

## 🛠️ Detalles de instalación y control de versiones

* **Rutas largas:**
  Si usas Windows, habilita el soporte a rutas largas en Git y el sistema para evitar problemas al versionar archivos grandes (ver la documentación del repo).

* **Dependencias:**
  Todas las dependencias están listadas en requirements.txt. Usa un entorno virtual para evitar conflictos.

---

## 🎓 Ejemplo de interpretación de resultados

* **Fitness alto + road rage bajo** = semáforo eficiente, menos tapón, menor estrés vial.

* **Fitness bajo + road rage alto** = semáforo deficiente, tapones frecuentes, oportunidades de mejora.

* Los gráficos muestran la evolución del desempeño a lo largo de las generaciones. ¡Tu objetivo es ver cómo el fitness sube y el road rage baja!

---

## 👨‍💻 Créditos y contacto
Proyecto desarrollado por Darwin Méndez, Michael García, Roither Sánchez y Camily García, en 2025.
Optimizaciones, integración de IA y organización del pipeline realizados junto a colaboración de herramientas IA y feedback de usuarios reales.