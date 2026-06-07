import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import google.generativeai as genai

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

# --- INICIALIZACIÓN DEL CEREBRO (GEMINI API) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_lista = True
except:
    api_lista = False

st.title("⚡ RODRIGO PERFORMANCE HUB")
st.markdown("---")

# --- ZONA DE CARGA UNIVERSAL (MULTIFORMATO) ---
archivos_subidos = st.file_uploader("📥 Arrastra aquí tus archivos (CSV, Capturas JPG/PNG, PDFs...)", accept_multiple_files=True)

# Variables Basales por defecto
hrv_actual = 39
body_battery = 61
sueno_puntuacion = 86
imagenes_cargadas = []

# Procesador de Inteligencia de Archivos
if archivos_subidos:
    for archivo in archivos_subidos:
        extension = archivo.name.split('.')[-1].lower()
        if extension == 'csv':
            try:
                df = pd.read_csv(archivo)
                if 'Puntuación' in df.columns:
                    hrv_actual = int(df.iloc[0]['Estado de VFC'])
                    body_battery = int(df.iloc[0]['Body Battery'])
                    sueno_puntuacion = int(df.iloc[0]['Puntuación'])
                    st.toast(f"✅ CSV Biométrico procesado: {archivo.name}")
                else:
                    st.toast(f"✅ CSV de Actividades detectado: {archivo.name}")
            except:
                st.toast(f"Error procesando CSV: {archivo.name}", icon="⚠️")
        elif extension in ['jpg', 'jpeg', 'png', 'heic']:
            imagenes_cargadas.append(archivo)
        elif extension == 'pdf':
            st.toast(f"📄 Documento PDF recibido: {archivo.name}")
        else:
            st.toast(f"📁 Archivo general guardado: {archivo.name}")

if imagenes_cargadas:
    with st.expander("📸 Archivos Multimedia Adjuntos (Haz clic para ver)", expanded=True):
        columnas_img = st.columns(len(imagenes_cargadas))
        for idx, img in enumerate(imagenes_cargadas):
            with columnas_img[idx]:
                st.image(img, caption=img.name, use_container_width=True)

st.markdown("---")

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
            st.write("**1. Zancadas peso corporal** (3 series x 20 reps)")
            st.markdown("*Garmin: Walking Lunge*")
            st.write("**2. Flexiones controladas** (3 series x 15 reps)")
            st.markdown("*Garmin: Push-Up*")
            st.write("**3. Remo mancuerna a un brazo** (3 series x 15 reps)")
            st.markdown("*Garmin: One-Arm Dumbbell Row*")
        else:
            st.success("**Fuerza Máxima Neural (Baja Repetición / Alto Peso)**")
            st.write("**1. Sentadilla Trasera con Barra** (4 series x 5 reps)")
            st.markdown("*Garmin: Barbell Back Squat*")
            st.write("**2. Peso Muerto Rumano** (3 series x 6 reps)")
            st.markdown("*Garmin: Romanian Deadlift*")
            st.write("**3. Dominadas Lastradas** (4 series x 5 reps)")
            st.markdown("*Garmin: Weighted Pull-Up*")
    elif "Carrera" in disciplina:
        st.info("Prescripción de carrera activa. (Restringido a Z2 si Luz Roja, abierto a Z5 si Luz Verde).")
    else:
        st.info("Actividad de bajo impacto o descanso seleccionado.")

# ==========================================
# PESTAÑA 2: CHAT INTELIGENTE NEURONAL
# ==========================================
with tab_chat:
    st.header("💬 Sala de Control Híbrida")
    st.write("Tu Coach analizará tu consulta teniendo en cuenta tus métricas actuales.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"¡Buenas Rodrigo! Tu VFC hoy es de {hrv_actual} ms. Si ya has configurado la clave API, pregúntame lo que necesites."}]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Escribe tu duda, pide un plan o reporta sensaciones..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            if api_lista:
                try:
                    # El System Prompt oculto que guía al Coach
                    instruccion_coach = f"""
                    Eres el entrenador de rendimiento híbrido de Rodrigo. Basa tus decisiones en ciencia (2021-2026), 
                    ignora rigideces obsoletas del ACSM y adapta el entreno a su VFC actual ({hrv_actual} ms). 
                    Responde de forma directa, técnica y empática a lo siguiente: {prompt}
                    """
                    respuesta_ia = model.generate_content(instruccion_coach)
                    st.markdown(respuesta_ia.text)
                    st.session_state.messages.append({"role": "assistant", "content": respuesta_ia.text})
                except Exception as e:
                    error_msg = f"Error en la conexión con Gemini: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                aviso = "⚠️ **Falta la conexión neuronal:** No has añadido la GOOGLE_API_KEY en los Secrets de Streamlit. Hazlo para que pueda responderte."
                st.warning(aviso)
                st.session_state.messages.append({"role": "assistant", "content": aviso})

# ==========================================
# PESTAÑAS 3 y 4: PLANES SEMANAL Y MENSUAL
# ==========================================
with tab_semana:
    st.header("🗓️ Plan Semanal")
    st.write("Estructura de la semana actual.")

with tab_mes:
    st.header("📊 Objetivos del Mes (Macrociclo)")
    st.write("Planificación mensual y focos estratégicos.")

# ==========================================
# PESTAÑA 5: HISTÓRICOS Y GRÁFICAS (INTACTAS)
# ==========================================
with tab_historicos:
    st.header("📈 Base de Datos Analítica (Últimas 52 Semanas)")
    
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

    # 1. ESTADO DE CARGA DE ENTRENO
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

    # 3. RITMOS POR ZONA CARDIACA
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

    # 4. KM RECORRIDOS Y VO2 MAX
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
