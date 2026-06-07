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

# --- CONFIGURACIÓN PASIVA DE LA API ---
api_configurada = False
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        api_configurada = True
    except Exception as e:
        st.sidebar.error(f"Error al configurar la llave: {e}")

st.title("⚡ RODRIGO PERFORMANCE HUB")
st.markdown("---")

# --- ZONA DE CARGA UNIVERSAL (MULTIFORMATO) ---
archivos_subidos = st.file_uploader("📥 Arrastra aquí tus archivos (CSV, Capturas JPG/PNG, PDFs...)", accept_multiple_files=True)

# Variables Basales por defecto
hrv_actual = 39
body_battery = 61
sueno_puntuacion = 86
imagenes_cargadas = []

# Procesador de Archivos
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
                    st.toast(f"✅ CSV Biométrico cargado: Métricas actualizadas", icon="📈")
                else:
                    st.toast(f"✅ CSV de Actividades detectado: {archivo.name}", icon="🏃‍♂️")
            except:
                st.toast(f"Error leyendo el CSV: {archivo.name}", icon="⚠️")
        elif extension in ['jpg', 'jpeg', 'png', 'heic']:
            imagenes_cargadas.append(archivo)
            st.toast(f"✅ Imagen guardada en memoria", icon="📸")
        else:
            st.toast(f"📁 Archivo recibido: {archivo.name}")

if imagenes_cargadas:
    with st.expander("📸 Ver Archivos Multimedia Adjuntos", expanded=False):
        columnas_img = st.columns(len(imagenes_cargadas))
        for idx, img in enumerate(imagenes_cargadas):
            with columnas_img[idx]:
                st.image(img, caption=img.name, use_container_width=True)

st.markdown("---")

# --- PESTAÑAS DE NAVEGACIÓN ---
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
        st.markdown("<div class='semaforo-rojo'><b>🔴 LUZ ROJA: Fatiga Central Detectada.</b><br>SNC deprimido. Evitar fallo muscular y series anaeróbicas lactácidas. Priorizar zona 2, flujo sanguíneo y recuperación activa.</div>", unsafe_allow_html=True)
    elif hrv_actual <= 45:
        st.markdown("<div class='semaforo-amarillo'><b>🟡 LUZ AMARILLA: Precaución.</b><br>Capacidad moderada. Entrenar con volumen e intensidad controlados. Dejar 2-3 repeticiones en recámara (RIR 2-3).</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='semaforo-verde'><b>🟢 LUZ VERDE: SNC Óptimo.</b><br>Tolerancia máxima al estrés. Vía libre para hipertrofia pesada, fuerza máxima neural o intervalos de VO2Max en carrera.</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("🏃‍♂️ Prescripción Dinámica de la Sesión")
    disciplina = st.selectbox("¿Qué disciplina vas a entrenar hoy?", ["🏃‍♂️ Carrera / Trail", "🏋️‍♂️ Gimnasio", "🧗‍♂️ Escalada (Rocódromo)", "🧘‍♂️ Descanso Activo"])
    
    if "Gimnasio" in disciplina:
        if hrv_actual < 40:
            st.info("**Objetivo: Fuerza Metabólica / Recuperación (Alta Repetición / Bajo Peso)**")
            st.write("1. **Zancadas peso corporal** (3 series x 20 reps)")
            st.write("2. **Flexiones controladas** (3 series x 15 reps)")
            st.write("3. **Remo con mancuerna** (3 series x 15 reps)")
        else:
            st.success("**Objetivo: Fuerza Máxima / Hipertrofia (Alta Carga / Tensión Mecánica)**")
            st.write("1. **Sentadilla Trasera con Barra** (4 series x 5-8 reps)")
            st.write("2. **Peso Muerto Rumano** (3 series x 8-10 reps)")
            st.write("3. **Dominadas Lastradas** (4 series x 5-6 reps)")
            
    elif "Carrera" in disciplina:
        if hrv_actual < 40:
            st.info("**Objetivo: Regenerativo. Carrera continua suave estricta en Z2 (<148 ppm). Evitar desniveles fuertes.**")
        else:
            st.success("**Objetivo: Desarrollo de VO2 Max. Series de 400m en pista o cuestas cortas (Z4/Z5).**")
            
    else:
        st.info("Prioridad: Movilidad articular, estiramientos suaves o descanso total. Escucha a tu cuerpo.")

# ==========================================
# PESTAÑA 2: CHAT INTELIGENTE NEURONAL
# ==========================================
with tab_chat:
    st.header("💬 AI Coach Híbrido (Multi-Modelo de Respaldo)")
    st.write("Plantea tus dudas de entrenamiento o reporta tus sensaciones. El sistema buscará automáticamente el canal gratuito activo en Europa.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"¡Hola Rodrigo! Conexión Free Tier reconfigurada. Tu VFC de hoy es de {hrv_actual} ms. ¿Qué aspecto de tu rendimiento quieres optimizar hoy?"}]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Escribe aquí tu consulta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            if api_configurada:
                contexto_base = f"""
                Eres el entrenador de rendimiento deportivo híbrido de Rodrigo.
                Datos fisiológicos de hoy de Rodrigo: HRV: {hrv_actual}ms, Body Battery: {body_battery}, Calidad Sueño: {sueno_puntuacion}.
                Basa tus consejos en la fisiología del ejercicio moderna. Sé conciso, técnico pero muy directo.
                Responde a lo siguiente: {prompt}
                """
                
                respuesta_conseguida = False
                errores_acumulados = ""
                
                # Lista con los nombres técnicos exactos requeridos por la versión API v1beta
                modelos_a_probar = ['gemini-1.5-flash-latest', 'gemini-1.5-flash-002', 'gemini-1.5-pro-latest', 'gemini-1.5-pro-002']
                
                for nombre_modelo in modelos_a_probar:
                    try:
                        model = genai.GenerativeModel(nombre_modelo)
                        respuesta_ia = model.generate_content(contexto_base)
                        st.markdown(respuesta_ia.text)
                        st.session_state.messages.append({"role": "assistant", "content": respuesta_ia.text})
                        respuesta_conseguida = True
                        break  # Si funciona, rompemos el bucle
                    except Exception as e_modelo:
                        errores_acumulados += f"• {nombre_modelo}: {str(e_modelo)}\n"
                        continue
                
                if not respuesta_conseguida:
                    st.error("❌ Todos los modelos de la capa gratuita devolvieron un error de conexión.")
                    with st.expander("🔍 Ver registro técnico de errores para diagnóstico"):
                        st.code(errores_acumulados)
            else:
                st.warning("⚠️ La API Key no está configurada en los Secrets de Streamlit.")

# ==========================================
# PESTAÑAS 3 y 4: PLANES SEMANAL Y MENSUAL
# ==========================================
with tab_semana:
    st.header("🗓 nighttime Microciclo Semanal")
    st.write("Estructura de la semana actual. Sube tu CSV de calendario para actualizar.")

with tab_mes:
    st.header("📊 Macrociclo Mensual")
    st.write("Focos estratégicos del mes.")

# ==========================================
# PESTAÑA 5: HISTÓRICOS Y GRÁFICAS
# ==========================================
with tab_historicos:
    st.header("📈 Base de Datos Analítica")
    
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

    st.subheader("1. Estado de Carga de Entrenamiento (Aguda vs Crónica)")
    fig_carga = go.Figure()
    fig_carga.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['Carga_Cronica'], fill='tozeroy', mode='none', name='Rango Óptimo (Crónica)', fillcolor='rgba(47, 133, 90, 0.4)'))
    fig_carga.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['Carga_Aguda'], mode='lines', name='Carga Actual (Aguda)', line=dict(color='#ff4b4b', width=2)))
    fig_carga.update_layout(template="plotly_dark", yaxis_title="Nivel de Carga", legend=dict(orientation="h", y=1.05))
    st.plotly_chart(fig_carga, use_container_width=True)

    st.subheader("2. Evolución VFC y Frecuencia Cardíaca en Reposo")
    fig_salud = px.line(df_anual, x='Fecha', y=['HRV', 'FC_Reposo'], color_discrete_map={'HRV': '#ff4b4b', 'FC_Reposo': '#4299e1'}, template="plotly_dark")
    fig_salud.update_layout(yaxis_title="ms / ppm", legend_title_text="Métrica")
    st.plotly_chart(fig_salud, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("3. Ritmos por Zona Cardiaca")
        tabla_ritmos = pd.DataFrame({
            "Zona": ["Zona 1 (<130 ppm)", "Zona 2 (131-148)", "Zona 3 (149-162)", "Zona 4 (163-175)", "Zona 5 (>176 ppm)"],
            "Ritmo Medio (min/km)": ["6:25", "5:40", "5:05", "4:30", "3:55"]
        })
        st.dataframe(tabla_ritmos, hide_index=True, use_container_width=True)

    with c2:
        st.subheader("4. Progresión Escalada (Grado)")
        fig_escalada = go.Figure()
        fig_escalada.add_trace(go.Scatter(x=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'], y=[3, 3, 4, 4, 5, 5], mode='lines+markers', name='Bloque (V)', line=dict(color='#ff9900', width=3)))
        fig_escalada.update_layout(template="plotly_dark", yaxis_title="Grado", margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_escalada, use_container_width=True)
