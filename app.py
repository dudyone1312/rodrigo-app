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
    .semaforo-verde { background-color: #22543d; border-left: 5px solid #48bb78; padding: 15px; border-radius: 5px; }
    .semaforo-amarillo { background-color: #744210; border-left: 5px solid #ecc94b; padding: 15px; border-radius: 5px; }
    .semaforo-rojo { background-color: #742a2a; border-left: 5px solid #f56565; padding: 15px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ RODRIGO PERFORMANCE HUB")
st.markdown("---")

# --- ZONA DE CARGA Y VARIABLES BASALES ---
uploaded_file = st.file_uploader("📥 Arrastra aquí tu CSV de Garmin", type=["csv"])

hrv_actual = 39
body_battery = 61
sueno_puntuacion = 86

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if 'Puntuación' in df.columns:
            hrv_actual = int(df.iloc[0]['Estado de VFC'])
            body_battery = int(df.iloc[0]['Body Battery'])
            sueno_puntuacion = int(df.iloc[0]['Puntuación'])
    except:
        pass

# --- PESTAÑAS ---
tab_hoy, tab_chat, tab_semana, tab_mes, tab_historicos = st.tabs([
    "🎯 HOY", "💬 AI COACH", "📅 PLAN SEMANAL", "📊 PLAN MENSUAL", "📈 HISTÓRICOS Y GRÁFICAS"
])

# ==========================================
# PESTAÑA 1: HOY (ESTADO Y SEMÁFORO)
# ==========================================
with tab_hoy:
    st.header("📊 Estatus del Atleta")
    c1, c2, c3 = st.columns(3)
    c1.metric(label="Variabilidad Cardíaca (HRV)", value=f"{hrv_actual} ms")
    c2.metric(label="Body Battery", value=f"{body_battery}/100")
    c3.metric(label="Calidad del Sueño", value=f"{sueno_puntuacion}/100")
    
    st.subheader("🚥 Semáforo de Predisposición de Carga")
    if hrv_actual < 40:
        st.markdown("<div class='semaforo-rojo'><b>🔴 LUZ ROJA: Fatiga Central Detectada.</b><br>El SNC está deprimido. Evitar RIR bajos (fallo muscular) y series anaeróbicas. Priorizar flujo sanguíneo y recuperación activa.</div>", unsafe_allow_html=True)
    elif hrv_actual <= 45:
        st.markdown("<div class='semaforo-amarillo'><b>🟡 LUZ AMARILLA: Precaución.</b><br>Capacidad moderada. Entrenar con volumen e intensidad controlados. RPE máximo de 7.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='semaforo-verde'><b>🟢 LUZ VERDE: SNC Óptimo.</b><br>Tolerancia máxima al estrés. Vía libre para hipertrofia pesada, fuerza máxima o intervalos de VO2Max.</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("🏃‍♂️ Prescripción de Sesión")
    disciplina = st.selectbox("¿Qué disciplina toca hoy?", ["🏃‍♂️ Carrera / Trail", "🏋️‍♂️ Gimnasio", "🧗‍♂️ Otros (Rocódromo)", "🧘‍♂️ Descanso"])
    
    if "Gimnasio" in disciplina:
        if hrv_actual < 40:
            st.info("**Fuerza Metabólica (Alta Repetición / Bajo Peso)**")
            st.write("**1. Zancadas peso corporal** (3x20) - *Garmin: Walking Lunge*")
            st.write("**2. Flexiones controladas** (3x15) - *Garmin: Push-Up*")
            st.write("**3. Remo mancuerna** (3x15) - *Garmin: One-Arm Dumbbell Row*")
        else:
            st.success("**Fuerza Máxima Neural (Baja Repetición / Alto Peso)**")
            st.write("**1. Sentadilla Trasera** (4x5) - *Garmin: Barbell Back Squat*")
            st.write("**2. Peso Muerto Rumano** (3x6) - *Garmin: Romanian Deadlift*")
            st.write("**3. Dominadas Lastradas** (4x5) - *Garmin: Weighted Pull-Up*")
    elif "Carrera" in disciplina:
        st.info("Prescripción de carrera activa. (Restringido a Z2 si Luz Roja, abierto a Z5 si Luz Verde).")
    else:
        st.info("Actividad de bajo impacto o descanso seleccionado.")

# ==========================================
# PESTAÑA 2: CHAT INTERACTIVO RESTAURADO
# ==========================================
with tab_chat:
    st.header("💬 Sala de Control Híbrida")
    st.write("Discute los entrenamientos o reporta fatiga. (API pendiente de conexión real).")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "¡Buenas Rodrigo! Semáforo en rojo hoy por los 39 ms. ¿Cómo tienes el estómago y las piernas tras el salmón de ayer?"}]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Escribe a tu coach..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Placeholder del Coach
        reply = "*(Sistema)*: Mensaje recibido. En cuanto inyectemos la API Key, este mensaje será generado automáticamente por tu IA analizando tu fisiología."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

# ==========================================
# PESTAÑAS 3 y 4 (Semanales y Mensuales)
# ==========================================
with tab_semana:
    st.header("🗓️ Plan Semanal")
    st.write("Estructura en construcción.")

with tab_mes:
    st.header("📊 Objetivos del Mes (Macrociclo)")
    st.write("Objetivos de Carrera y Gimnasio mes a mes.")

# ==========================================
# PESTAÑA 5: HISTÓRICOS (EL NÚCLEO DE DATOS)
# ==========================================
with tab_historicos:
    st.header("📈 Base de Datos Analítica (Últimas 52 Semanas)")
    
    # Generación de datos anuales simulados para pintar las gráficas
    fechas_anual = pd.date_range(end=datetime.date(2026, 6, 6), periods=52, freq='W')
    df_anual = pd.DataFrame({
        'Fecha': fechas_anual,
        'HRV': np.random.randint(35, 60, size=52),
        'FC_Reposo': np.random.randint(48, 58, size=52),
        'Km': np.random.randint(15, 50, size=52),
        'VO2Max': np.linspace(46, 51, 52) + np.random.normal(0, 0.5, 52),
        'Carga_Aguda': np.random.randint(400, 800, size=52),
        'Carga_Cronica': np.random.randint(450, 700, size=52)
    })

    # 1. CARGA DE ENTRENAMIENTO ESTILO GARMIN
    st.subheader("1. Estado de Carga de Entrenamiento (Aguda vs Crónica)")
    fig_carga = go.Figure()
    fig_carga.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['Carga_Cronica'], fill='tozeroy', mode='none', name='Rango Óptimo (Crónica)', fillcolor='rgba(47, 133, 90, 0.4)'))
    fig_carga.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['Carga_Aguda'], mode='lines', name='Carga Actual (Aguda)', line=dict(color='#ff4b4b', width=2)))
    fig_carga.update_layout(template="plotly_dark", yaxis_title="Nivel de Carga", legend=dict(orientation="h", y=1.05))
    st.plotly_chart(fig_carga, use_container_width=True)

    # 2. VFC Y FC REPOSO
    st.subheader("2. Evolución VFC y Frecuencia Cardíaca en Reposo")
    fig_salud = px.line(df_anual, x='Fecha', y=['HRV', 'FC_Reposo'], color_discrete_map={'HRV': '#ff4b4b', 'FC_Reposo': '#4299e1'}, template="plotly_dark")
    fig_salud.update_layout(yaxis_title="ms / ppm", legend_title_text="Métrica")
    st.plotly_chart(fig_salud, use_container_width=True)

    # 3. RITMOS POR ZONA CARDIACA (Tabla Semana/Mes)
    st.subheader("3. Ritmos Medios (min/km) por Zona Cardiaca (Mes Actual)")
    tabla_ritmos = pd.DataFrame({
        "Periodo": ["Semana 1 (Junio)", "Semana 2 (Junio)", "Semana 3 (Junio)", "Mes Promedio (Mayo)"],
        "Zona 1 (<130 ppm)": ["6:30", "6:25", "6:20", "6:40"],
        "Zona 2 (131-148)": ["5:45", "5:40", "5:35", "5:55"],
        "Zona 3 (149-162)": ["5:10", "5:05", "5:00", "5:15"],
        "Zona 4 (163-175)": ["4:35", "4:30", "4:28", "4:40"],
        "Zona 5 (>176 ppm)": ["4:00", "3:55", "3:50", "4:10"]
    })
    st.dataframe(tabla_ritmos, hide_index=True, use_container_width=True)

    # 4. KILÓMETROS Y VO2 MAX
    st.subheader("4. Kilómetros Recorridos y VO2 Max")
    fig_km = go.Figure()
    fig_km.add_trace(go.Bar(x=df_anual['Fecha'], y=df_anual['Km'], name='Volumen (Km)', marker_color='#4a5568'))
    fig_km.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['VO2Max'], name='VO2 Max', yaxis='y2', mode='lines+markers', line=dict(color='#ecc94b', width=3)))
    fig_km.update_layout(
        template="plotly_dark",
        yaxis=dict(title="Kilómetros"),
        yaxis2=dict(title="VO2 Max", overlaying="y", side="right", range=[40, 55]),
        legend=dict(orientation="h", y=1.05)
    )
    st.plotly_chart(fig_km, use_container_width=True)

    # 5. CARGAS GIMNASIO
    st.subheader("5. Evolución de Cargas en Gimnasio")
    datos_fuerza = pd.DataFrame({
        "Grupo Muscular": ["Pierna", "Cadena Posterior", "Espalda", "Pecho/Hombro"],
        "Ejercicio": ["Sentadilla Trasera", "Peso Muerto", "Dominadas Lastradas", "Press Banca"],
        "Series x Reps": ["4 x 5", "3 x 5", "4 x 6", "3 x 8"],
        "Peso Actual": ["100 kg", "120 kg", "+15 kg", "75 kg"],
        "Peso Anterior": ["95 kg", "110 kg", "+10 kg", "70 kg"],
        "Última Actualización": ["01 Jun 2026", "03 Jun 2026", "28 May 2026", "29 May 2026"]
    })
    st.dataframe(datos_fuerza, hide_index=True, use_container_width=True)

    # 6. GRADOS EN ROCO
    st.subheader("6. Progresión en Escalada (Rocódromo)")
    meses_escalada = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    fig_escalada = go.Figure()
    fig_escalada.add_trace(go.Scatter(x=meses_escalada, y=[3, 3, 4, 4, 5, 5], mode='lines+markers', name='Bloque (Escala V)', line=dict(color='#ff9900', width=3)))
    fig_escalada.add_trace(go.Scatter(x=meses_escalada, y=[4, 5, 5, 6, 6, 7], mode='lines+markers', name='Deportiva (Grado Relativo)', line=dict(color='#00cc99', width=3)))
    fig_escalada.update_layout(template="plotly_dark", yaxis_title="Nivel de Grado", legend=dict(orientation="h", y=1.05))
    st.plotly_chart(fig_escalada, use_container_width=True)
