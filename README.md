# 📡 Cálculo del Tiempo de Transferencia de Datos entre Servidores (TFC)

Aplicación interactiva desarrollada en **Streamlit** que implementa y visualiza la aplicación práctica del **Teorema Fundamental del Cálculo (TFC)** para calcular el tiempo de transferencia de archivos a través de redes de computadores con tasas de velocidad variables.

---

## 📐 Fundamentación Matemática

La transferencia de un volumen total de datos $D_{\text{total}}$ a través de una red cuya velocidad instantánea $R(t)$ varía en el tiempo se modela mediante la integral definida:

$$\int_{0}^{T} R(t) \, dt = D_{\text{total}}$$

* **$R(t)$**: Tasa instantánea de transferencia en Mbps.
* **$D_{\text{total}}$**: Volumen total de datos expresado en Megabits.
* **$T$**: Tiempo total transcurrido en segundos necesario para completar la transferencia.

La aplicación utiliza integración numérica mediante la **Regla del Trapecio** para evaluar el área acumulada bajo la curva de transferencia $R(t)$ hasta alcanzar $D_{\text{total}}$.

---

## 🚀 Características

* **Ajuste en tiempo real:** Selección del tamaño del archivo (GB), velocidad base de red (Mbps) y variabilidad por congestión (%).
* **Simulación realista:** Generación de fluctuaciones de velocidad mediante ondas sinusoidales y ruido estocástico.
* **Visualización interactiva:** Gráfico interactivo construido con Plotly que representa el área bajo la curva (integral).
* **Métricas clave:** Cálculo automático del tiempo estimado ($T$), velocidad promedio y tasa máxima alcanzada.

---

## 🛠️ Requisitos Previos

Asegúrate de tener instalado Python 3.8 o superior en tu sistema.

---

## 📦 Instalación y Ejecución Local

Sigue estos pasos para ejecutar la aplicación en tu equipo local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/TU_REPOSITTORIO.git](https://github.com/TU_USUARIO/TU_REPOSITTORIO.git)
   cd TU_REPOSITORIO
