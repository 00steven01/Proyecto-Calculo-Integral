import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Transferencia de Datos - TFC", layout="wide", page_icon="📡")

# Estilo y Título Principal
st.title("📡 Cálculo del Tiempo de Transferencia de Datos entre Servidores")
st.caption("Aplicación práctica del Teorema Fundamental del Cálculo (TFC) en redes de computadores.")

st.markdown("""
Esta aplicación evalúa el tiempo $T$ requerido para transferir un volumen de datos $D_{\\text{total}}$ a través de una red por cable Ethernet, donde la tasa de transferencia $R(t)$ varía en función del tiempo.

$$\\int_{0}^{T} R(t) \, dt = D_{\\text{total}}$$
""")

# --- BARRA LATERAL: PARÁMETROS DE ENTRADA ---
st.sidebar.header("⚙ Parámetros de Entrada")

tamano_gb = st.sidebar.number_input(
    "Tamaño del archivo a enviar (GB):",
    min_value=0.1,
    max_value=1000.0,
    value=50.0,
    step=5.0
)

velocidad_base = st.sidebar.slider(
    "Velocidad base del cable (Mbps):",
    min_value=100,
    max_value=1000,
    value=850,
    step=50
)

variabilidad = st.sidebar.slider(
    "Variabilidad por congestión/disco (%):",
    min_value=0,
    max_value=50,
    value=15
)

# Conversión a Megabits (1 GB = 8000 Mb en escala decimal estándar de red)
tamano_mbits = tamano_gb * 8000

# --- SIMULACIÓN DEL PERFIL DE VELOCIDAD R(t) ---
# Se genera una ventana temporal de hasta 4 horas (14400 segundos)
tiempo_seg = np.arange(0, 14400, 1)

# Modelo matemático de velocidad oscilante por variaciones de tráfico y lectura de disco
amp = velocidad_base * (variabilidad / 100)
velocidad_mbps = velocidad_base + amp * np.sin(2 * np.pi * tiempo_seg / 600) + np.random.normal(0, 5, len(tiempo_seg))
velocidad_mbps = np.maximum(velocidad_mbps, 10.0)  # Garantizar velocidad mínima positiva

# --- INTEGRACIÓN NUMÉRICA (REGLA DE TRAPECIOS) ---
# Evaluación del área bajo la curva término a término mediante suma acumulativa
incrementos = (velocidad_mbps[:-1] + velocidad_mbps[1:]) * 0.5 * np.diff(tiempo_seg)
datos_acumulados_mbits = np.concatenate(([0.0], np.cumsum(incrementos)))

# Búsqueda del límite superior T
indice_final = np.argmax(datos_acumulados_mbits >= tamano_mbits)

if datos_acumulados_mbits[-1] < tamano_mbits:
    st.error("❌ El tamaño del archivo es demasiado grande para el rango de tiempo simulado.")
else:
    tiempo_total_seg = tiempo_seg[indice_final]
    minutos = int(tiempo_total_seg // 60)
    segundos = int(tiempo_total_seg % 60)

    # Submuestero de datos para la gráfica
    t_corte = tiempo_seg[:indice_final+1]
    v_corte = velocidad_mbps[:indice_final+1]

    # --- RESULTADOS Y MÉTRICAS ---
    st.subheader("📊 Resultados de la Transferencia")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Datos Totales (D)", f"{tamano_gb:.1f} GB", f"{tamano_mbits:,.0f} Mb")
    c2.metric("Tiempo Estimado (T)", f"{minutos} min {segundos} s", f"{tiempo_total_seg:.0f} segundos")
    c3.metric("Velocidad Promedio", f"{v_corte.mean():.2f} Mbps")
    c4.metric("Tasa Máxima Alcanzada", f"{v_corte.max():.2f} Mbps")

    st.markdown("---")

    # --- GRÁFICO INTERACTIVO ---
    st.subheader("📈 Representación Gráfica de la Integral")

    fig = go.Figure()

    # Área bajo la curva (Integral de la velocidad)
    fig.add_trace(go.Scatter(
        x=t_corte / 60,
        y=v_corte,
        mode='lines',
        name='Tasa R(t) [Mbps]',
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.3)',
        line=dict(color='#1f77b4', width=2)
    ))

    fig.update_layout(
        title=f"Área bajo la curva = Volume de datos transferidos ({tamano_gb} GB)",
        xaxis_title="Tiempo transcurrido (Minutos)",
        yaxis_title="Tasa de Transferencia R(t) [Mbps]",
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- FUNDAMENTACIÓN TEÓRICA ---
    with st.expander("📚 Justificación Teórica: Teorema Fundamental del Cálculo"):
        st.markdown("""
        ### Relación entre el Teorema y la Red

        1. **Primera parte del TFC (Función Acumuladora):**
           La velocidad instantánea $R(t)$ representa la tasa de cambio o derivada temporal de la cantidad de datos $D(t)$:
           $$\\frac{d}{dt}[D(t)] = R(t)$$

        2. **Segunda parte del TFC (Evaluación del Límite Superior $T$):**
           Para encontrar el tiempo total $T$ que le toma a la red transferir la totalidad de los Megabits requeridos $D_{\\text{total}}$, evaluamos la integral definida:
           $$D_{\\text{total}} = \\int_{0}^{T} R(t) \, dt$$

        Mediante métodos numéricos (Regla de Trapecios en Python), la aplicación acumula el área de la tasa de transferencia segundo a segundo hasta que alcanza $D_{\\text{total}}$, obteniendo así el valor de $T$.
        """)
