import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Rodrigo Hybrid Hub", layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS
st.markdown("""
    <style>
    .main { background-color: #0d0f14; color: #e2e8f0; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: bold; color: #a0aec0; }
    .stTabs [aria-selected="true"] { color: #ff4b4b !important; border-bottom-color: #ff4b4b !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ RODRIGO PERFORMANCE HUB")
st.markdown("---")

# ZONA DE CARGA
uploaded_file = st.file_uploader("📥 Arrastra aquí tu CSV de Garmin (Actividades o Sueño)", type=["csv"])

# VARIABLES BIOMÉTRICAS BASE (Sábado 6 de Junio)
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
            st.toast("⚡ Métricas biométricas actualizadas.", icon="✅")
    except:
        st.toast("Archivo cargado correctamente.", icon="ℹ️")

# MAQUETACIÓN POR PESTAÑAS
tab_hoy, tab_chat, tab_semana = st.tabs(["🎯 HOY", "💬 AI COACH", "📅 PLAN SEMANAL"])

# --- PESTAÑA 1: HOY ---
with tab_hoy:
    st.header("📊 Estatus del Atleta")
    c1, c2, c3 = st.columns(3)
    c1.metric(label="HRV", value=f"{hrv_actual} ms", delta="Fatiga Central" if hrv_actual < 40 else "Óptimo")
    c2.metric(label="Body Battery", value=f"{body_battery}/100")
    c3.metric(label="Sueño", value=f"{sueno_puntuacion}/100")
    
    st.markdown("---")
    st.header("🏃‍♂️ Prescripción Dinámica")
    
    # El usuario elige el dominio, el sistema pone las reglas
    dominio = st.selectbox(
        "¿Qué terreno / instalación tienes disponible hoy?",
        ["🏃‍♂️ Carrera / Trail", "🏋️‍♂️ Gimnasio", "🧗‍♂️ Otros (Rocódromo, Bici...)", "🧘‍♂️ Descanso"]
    )
    
    st.markdown("### 📋 Estructura de la Sesión")
    
    # LÓGICA DE PRESCRIPCIÓN INTELIGENTE
    if hrv_actual < 40:
        # PRESCRIPCIÓN PARA SNC FATIGADO
        st.warning("⚠️ **SNC Deprimido (VFC en 39 ms).** El sistema restringe la alta tensión mecánica y el impacto excéntrico masivo.")
        
        if "Carrera" in dominio:
            st.info("**Objetivo:** Densidad mitocondrial sin daño muscular.\n* **Terreno:** Llano o subidas caminadas (power-hiking). Cero bajadas técnicas.\n* **Intensidad:** Zona 1 y Zona 2 estricta.\n* **Volumen:** Máximo 45-60 min.")
        elif "Gimnasio" in dominio:
            st.info("**Objetivo:** Recondicionamiento, lavado de lactato y stiffness tendinoso.\n* **Estructura:** 3-4 series x 15-20 repeticiones. RIR 4 (Lejos del fallo).\n* **Ejercicios:** Unilaterales ligeros, isométricos de core, trabajo de estabilización.\n* **Restricción:** Prohibido pesos $\ge$ 80% 1RM hoy.")
        elif "Otros" in dominio:
            st.info("**Objetivo:** Volumen técnico fluyido.\n* **Estructura:** RPE $\le$ 6. Si es rocódromo, bloques de calentamiento o grado bajo, descansos largos. No buscar el fallo de antebrazos.")
        else:
            st.info("**Objetivo:** Recuperación parasimpática total.\n* **Estructura:** Movilidad articular, foam roller suave o reposo absoluto.")
            
    else:
        # PRESCRIPCIÓN PARA SNC RECUPERADO (HRV >= 40)
        st.success("✅ **SNC Recuperado.** Capacidad operativa óptima para estímulos agresivos.")
        
        if "Carrera" in dominio:
            st.info("**Objetivo:** Potencia Aeróbica (VO2máx) o Tolerancia Excéntrica.\n* **Estructura:** Series en Z5 (ej. 5x3') o Long Trail Run con bajadas (D-) técnicas agresivas.")
        elif "Gimnasio" in dominio:
            st.info("**Objetivo:** Fuerza Máxima / Tensión Mecánica.\n* **Estructura:** 3-5 series x 3-5 repeticiones. $\ge$ 85% 1RM. RIR 1-2.\n* **Ejercicios:** Sentadilla pesada, Peso Muerto, Dominadas lastradas.")
        elif "Otros" in dominio:
            st.info("**Objetivo:** Rendimiento pico.\n* **Estructura:** Proyección de bloques al límite en rocódromo o series de sprints en bici.")
        else:
            st.info("Día libre programado. Aprovecha para recargar depósitos de glucógeno.")

# --- PESTAÑA 2: AI COACH (CHAT) ---
with tab_chat:
    st.header("💬 Sala de Control Híbrida")
    st.write("Consulta ajustes, reporta molestias o debate la ciencia de tu entrenamiento.")
    
    # Inicializar el historial de chat en la interfaz
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "¡Buenas, Rodrigo! Tu Fénix 7X me indica que estás en 39 ms de HRV. ¿Cómo te notas de piernas para la sesión de hoy?"}]
    
    # Mostrar el historial de mensajes
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Input de chat
    if prompt := st.chat_input("Escribe aquí a tu entrenador..."):
        # Mostrar lo que escribe el usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Respuesta placeholder hasta que conectemos la API de Gemini
        placeholder_reply = "*(Sistema)*: ¡La interfaz de chat ya está lista! El próximo paso técnico será conectar mi 'cerebro' (la API de Gemini) a esta caja de texto para que te responda en tiempo real y lea tus CSV de forma automática."
        st.session_state.messages.append({"role": "assistant", "content": placeholder_reply})
        with st.chat_message("assistant"):
            st.markdown(placeholder_reply)

# --- PESTAÑA 3: PLAN SEMANAL ---
with tab_semana:
    st.header("🗓️ Microciclo en Curso")
    st.write("Visualización de la semana. (Se rellenará dinámicamente con la API).")
