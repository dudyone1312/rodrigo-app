import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime

# --- CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="Rodrigo Hybrid Hub", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main { background-color: #0d0f14; color: #e2e8f0; }
    .stTabs [data-baseweb="tab"] { font-size: 15px; font-weight: bold; color: #a0aec0; }
    .stTabs [aria-selected="true"] { color: #ff4b4b !important; border-bottom-color: #ff4b4b !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ RODRIGO PERFORMANCE HUB")
st.markdown("---")

# --- VARIABLES BASALES ---
hrv_actual = 39
body_battery = 61
sueno_puntuacion = 86

# --- PESTAÑAS ---
tab_hoy, tab_chat, tab_semana, tab_mes, tab_historicos = st.tabs([
    "🎯 HOY", "💬 AI COACH", "📅 PLAN SEMANAL", "📊 PLAN MENSUAL", "📈 HISTÓRICOS Y GRÁFICAS"
])

# ==========================================
# PESTAÑA 1: HOY (CON TRADUCTOR GARMIN)
# ==========================================
with tab_hoy:
    st.header("📋 Prescripción de Entrenamiento")
    
    disciplina = st.selectbox(
        "¿Qué bloque toca hoy?",
        ["🏃‍♂️ Carrera / Trail Running", "🏋️‍♂️ Gimnasio / Sala de Fuerza", "🧗‍♂️ Otros (Rocódromo, Ciclismo...)", "🧘‍♂️ Descanso Activo"]
    )
    
    st.markdown("### 📋 Estructura de la Sesión")
    
    if "Gimnasio" in disciplina:
        if hrv_actual < 40:
            st.warning("⚠️ **SNC Deprimido:** Fuerza Metabólica de recondicionamiento (Altas reps, poco peso).")
            st.markdown("""
            **1. Zancadas caminando con peso corporal** (3 series x 20 reps)
            *Garmin: Walking Lunge*
            
            **2. Flexiones de pecho controladas** (3 series x 15 reps)
            *Garmin: Push-Up*
            
            **3. Remo con mancuerna a un brazo** (3 series x 15 reps)
            *Garmin: One-Arm Dumbbell Row*
            
            **4. Plancha frontal isométrica** (3 series x 45 seg)
            *Garmin: Plank*
            """)
        else:
            st.success("✅ **SNC Óptimo:** Fuerza Máxima y Tensión Mecánica (Bajas reps, peso alto).")
            st.markdown("""
            **1. Sentadilla Trasera con Barra** (4 series x 5 reps @ 85% 1RM)
            *Garmin: Barbell Back Squat*
            
            **2. Peso Muerto Rumano** (3 series x 6 reps)
            *Garmin: Romanian Deadlift*
            
            **3. Dominadas Lastradas** (4 series x 5 reps)
            *Garmin: Weighted Pull-Up*
            
            **4. Press de Hombros con Mancuernas** (3 series x 8 reps)
            *Garmin: Dumbbell Shoulder Press*
            """)
    elif "Carrera" in disciplina:
        st.info("Prescripción de carrera basada en tu HRV actual y objetivos de base aeróbica. Ritmos Z2.")
    else:
        st.info("Directrices de descanso o escalada de fluidez programadas.")

# ==========================================
# PESTAÑA 2, 3 y 4 (Estructura base mantenida)
# ==========================================
with tab_chat:
    st.header("💬 Sala de Control Híbrida")
    st.write("*(El motor de IA se conectará en el próximo paso)*")

with tab_semana:
    st.header("🗓️ Microciclo en Curso")
    st.write("Planificación semanal de lunes a domingo.")

with tab_mes:
    st.header("📊 Macrociclo")
    st.write("Vista de bloques mensuales sombreados.")

# ==========================================
# PESTAÑA 5: HISTÓRICOS (FUERZA, ESCALADA, ETC)
# ==========================================
with tab_historicos:
    st.header("📈 Panel de Rendimiento Integral")
    
    # 1. CUADRO DE FUERZA (NUEVO)
    st.subheader("🏋️‍♂️ Evolución de Cargas en Gimnasio")
    datos_fuerza = pd.DataFrame({
        "Grupo Muscular": ["Pierna (Cuádriceps)", "Cadena Posterior", "Tirones (Espalda)", "Empujes (Pecho/Hombro)"],
        "Ejercicio Principal": ["Sentadilla Trasera", "Peso Muerto", "Dominadas Lastradas", "Press Banca"],
        "Series x Reps": ["4 x 5", "3 x 5", "4 x 6", "3 x 8"],
        "Peso Actual": ["100 kg", "120 kg", "+15 kg", "75 kg"],
        "Peso Anterior": ["95 kg", "110 kg", "+10 kg", "70 kg"],
        "Fecha Anterior": ["15 May 2026", "10 May 2026", "18 May 2026", "20 May 2026"]
    })
    st.dataframe(datos_fuerza, hide_index=True, use_container_width=True)
    st.markdown("---")
    
    # 2. GRÁFICA DE ESCALADA (NUEVO)
    st.subheader("🧗‍♂️ Progresión en Escalada (Bloque vs Vertical)")
    st.write("*Gráfica de evolución mostrando el grado máximo consolidado por mes.*")
    
    meses_escalada = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    grado_bloque = [3, 3, 4, 4, 5, 5]     # Simulación: V3 a V5
    grado_vertical = [4, 5, 5, 6, 6, 7]   # Simulación: 5b, 5c, 6a...
    
    fig_escalada = go.Figure()
    fig_escalada.add_trace(go.Scatter(x=meses_escalada, y=grado_bloque, mode='lines+markers', name='Bloque (Escala V)', line=dict(color='#ff9900', width=3), marker=dict(size=8)))
    fig_escalada.add_trace(go.Scatter(x=meses_escalada, y=grado_vertical, mode='lines+markers', name='Vertical (Deportiva)', line=dict(color='#00cc99', width=3), marker=dict(size=8)))
    
    fig_escalada.update_layout(
        template="plotly_dark",
        yaxis_title="Nivel de Grado (Relativo)",
        xaxis_title="Meses",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_escalada, use_container_width=True)
    st.markdown("---")

    # 3. GRÁFICAS BASE (HRV y Carga mantenidas del código anterior de forma reducida para no saturar)
    st.subheader("❤️ Evolución VFC y Frecuencia en Reposo")
    fechas = pd.date_range(end=datetime.date(2026, 6, 6), periods=12, freq='W')
    data_hrv = pd.DataFrame({'Fecha': fechas, 'HRV': np.random.randint(35, 55, size=12), 'FC_Reposo': np.random.randint(48, 58, size=12)})
    fig_hrv = px.line(data_hrv, x='Fecha', y=['HRV', 'FC_Reposo'], color_discrete_map={'HRV': '#ff4b4b', 'FC_Reposo': '#4299e1'}, template="plotly_dark")
    st.plotly_chart(fig_hrv, use_container_width=True)
