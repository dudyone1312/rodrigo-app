import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import google.generativeai as genai

# --- 1. CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="Rodrigo Hybrid Hub", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding-top: 0.8rem; padding-bottom: 0rem; padding-left: 0.8rem; padding-right: 0.8rem; }
    h1 { font-size: 1.6rem !important; margin-bottom: 0rem !important; }
    h2 { font-size: 1.2rem !important; margin-top: 0.4rem !important; }
    .stTabs [data-baseweb="tab"] { font-size: 13px; padding: 5px 8px; }
    [data-testid="stMetricValue"] { font-size: 1.4rem !important; }
    .semaforo-box { border-radius: 6px; padding: 6px; color: white; text-align: center; font-size: 12px; }
    .semaforo-rojo { background-color: #742a2a; border: 1.5px solid #f56565; }
    .semaforo-amarillo { background-color: #744210; border: 1.5px solid #ecc94b; }
    .semaforo-verde { background-color: #22543d; border: 1.5px solid #48bb78; }
    [data-testid="stChatMessage"] { padding: 0.4rem; border-radius: 6px; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURACIÓN API ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 3. CABECERA ---
st.title("🏔️ RODRIGO HYBRID HUB")
st.markdown("---")

with st.expander("📥 Cargar Archivos (Garmin CSV/Fotos)", expanded=False):
    archivos_subidos = st.file_uploader("Arrastra aquí", accept_multiple_files=True, label_visibility="collapsed")

hrv_actual, body_battery, sueno_puntuacion = 39, 61, 86
if archivos_subidos:
    for f in archivos_subidos:
        if f.name.endswith('.csv'):
            try:
                df = pd.read_csv(f)
                if 'Puntuación' in df.columns:
                    hrv_actual, body_battery, sueno_puntuacion = int(df.iloc[0]['Estado de VFC']), int(df.iloc[0]['Body Battery']), int(df.iloc[0]['Puntuación'])
            except: pass

# --- 4. PESTAÑAS ---
tab_hoy, tab_chat, tab_analitica, tab_planes = st.tabs(["🎯 HOY", "💬 AI COACH", "📈 ANALÍTICA", "📅 PLANES"])

with tab_hoy:
    c_m, c_s = st.columns([1.4, 1])
    with c_m:
        st.subheader("📊 Estatus")
        col1, col2, col3 = st.columns(3)
        col1.metric("HRV", f"{hrv_actual} ms")
        col2.metric("Bat", f"{body_battery}/100")
        col3.metric("Sueño", f"{sueno_puntuacion}/100")
    with c_s:
        st.subheader("🚥 Predisposición")
        clase = "semaforo-rojo" if hrv_actual < 40 else "semaforo-amarillo" if hrv_actual <= 45 else "semaforo-verde"
        st.markdown(f"<div class='semaforo-box {clase}'><b>{'🔴 ROJO' if hrv_actual < 40 else '🟡 AMARILLO' if hrv_actual <= 45 else '🟢 VERDE'}</b></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    disciplina = st.selectbox("Entrenamiento:", ["🏃‍♂️ Carrera", "🏋️‍♂️ Gimnasio", "🧗‍♂️ Escalada", "🧘‍♂️ Descanso"])
    st.info("Recomendación de carga basada en tu estado fisiológico actual.")

with tab_chat:
    chat_input_container = st.container()
    messages_container = st.container()
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "¡Hola Rodrigo! Coach activo."}]
        
    with messages_container:
        for msg in reversed(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    with chat_input_container:
        if prompt := st.chat_input("Escribe tu duda..."):
            if any(x in prompt.lower() for x in ["borra", "limpia", "elimina"]):
                st.session_state.messages = []
                st.rerun()
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            try:
                # LÓGICA DE DESCUBRIMIENTO ANTI-404
                modelos = [m.name for m in genai.list_models() if "gemini-1.5-flash" in m.name and "generateContent" in m.supported_generation_methods]
                modelo_usar = modelos[0] if modelos else 'gemini-1.5-flash'
                
                paquete = [f"Coach deportivo. Rodrigo (HRV:{hrv_actual}, BB:{body_battery}). Consulta: {prompt}"]
                model = genai.GenerativeModel(modelo_usar)
                resp = model.generate_content(paquete)
                st.session_state.messages.append({"role": "assistant", "content": resp.text})
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"Fallo de conexión: {e}"})
            st.rerun()

with tab_analitica:
    st.subheader("📈 Analítica de Rendimiento")
    fechas = pd.date_range(end=datetime.date.today(), periods=52, freq='W')
    df = pd.DataFrame({'Fecha': fechas, 'HRV': np.random.randint(35, 60, size=52), 'Carga': np.random.randint(400, 800, size=52)})

    st.markdown("##### 1. Carga Aguda vs Crónica")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df['Fecha'], y=df['Carga'], mode='lines', line=dict(color='#ff4b4b')))
    fig1.update_layout(height=150, margin=dict(l=5,r=5,t=5,b=5), template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("##### 2. Evolución HRV")
    fig2 = px.line(df, x='Fecha', y='HRV', template="plotly_dark")
    fig2.update_layout(height=150, margin=dict(l=5,r=5,t=5,b=5))
    st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Ritmos Zona")
        st.table(pd.DataFrame({"Zona": ["Z2", "Z4"], "Ritmo": ["5:40", "4:30"]}))
    with col2:
        st.markdown("##### Progreso Escalada")
        st.line_chart([3, 4, 4, 5, 5])

with tab_planes:
    st.subheader("📅 Planificación")
    st.write("Estructura estratégica de bloques.")
