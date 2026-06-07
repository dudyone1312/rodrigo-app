import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import google.generativeai as genai

# --- 1. CONFIGURACIÓN E INTERFAZ (CSS ULTRA-COMPACTO) ---
st.set_page_config(page_title="Rodrigo Hybrid Hub", layout="wide", initial_sidebar_state="collapsed")

# CSS para forzar compactación en móvil y rediseño de chats
st.markdown("""
    <style>
    /* Compactación general de espacios */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; }
    h1 { font-size: 1.8rem !important; margin-bottom: 0rem !important; margin-top: 0rem !important; }
    h2 { font-size: 1.4rem !important; margin-top: 0.5rem !important; margin-bottom: 0.2rem !important; }
    h3 { font-size: 1.1rem !important; margin-top: 0.3rem !important; }
    .stTabs [data-baseweb="tab"] { font-size: 14px; padding-left: 10px; padding-right: 10px; }
    .stMetric { padding: 0px !important; margin: 0px !important; }
    .stMetric > div { padding: 0px !important; }
    [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
    [data-testid="stMetricLabel"] { font-size: 0.8rem !important; }
    div[data-testid="stToast"] { padding: 5px; font-size: 12px; }
    
    /* Semáforo visual compacto */
    .semaforo-box { border-radius: 8px; padding: 10px; color: white; text-align: center; }
    .semaforo-rojo { background-color: #742a2a; border: 2px solid #f56565; }
    .semaforo-amarillo { background-color: #744210; border: 2px solid #ecc94b; }
    .semaforo-verde { background-color: #22543d; border: 2px solid #48bb78; }
    
    /* Estilos del Chat */
    [data-testid="stChatMessage"] { padding: 0.5rem; margin-bottom: 0.5rem; border-radius: 8px; }
    
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURACIÓN PASIVA DE LA API ---
api_configurada = False
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        api_configurada = True
    except Exception:
        st.sidebar.error("Error en credenciales API")

# --- 3. CABECERA FIJA DE LA APP (FUERA DE LAS PESTAÑAS) ---
st.title("🏔️ RODRIGO HYBRID HUB")
st.markdown("---")

# Zona de carga universal (Compacta)
with st.expander("📥 Cargar Archivos (Garmin CSV/Fotos/PDF)", expanded=False):
    archivos_subidos = st.file_uploader("Arrastra aquí tus archivos", accept_multiple_files=True, label_visibility="collapsed")

# Variables Basales por defecto
hrv_actual = 39
body_battery = 61
sueno_puntuacion = 86
imagenes_cargadas = []

if archivos_subidos:
    for archivo in archivos_subidos:
        extension = archivo.name.split('.')[-1].lower()
        if extension == 'csv':
            try:
                archivo.seek(0)
                df = pd.read_csv(archivo)
                if 'Puntuación' in df.columns:
                    hrv_actual = int(df.iloc[0]['Estado de VFC'])
                    body_battery = int(df.iloc[0]['Body Battery'])
                    sueno_puntuacion = int(df.iloc[0]['Puntuación'])
                    st.toast(f"✅ Biométricos actualizados", icon="📈")
                else:
                    st.toast(f"✅ CSV detectado: {archivo.name}", icon="🏃‍♂️")
            except Exception: pass
        elif extension in ['jpg', 'jpeg', 'png']:
            imagenes_cargadas.append(archivo)
            st.toast(f"✅ Imagen guardada", icon="📸")

# --- 4. PESTAÑAS DE NAVEGACIÓN PRINCIPAL ---
tab_hoy, tab_chat, tab_historicos, tab_planes = st.tabs([
    "🎯 HOY", "💬 AI COACH", "📈 ANALÍTICA", "📅 PLANES"
])

# ==========================================
# PESTAÑA 1: HOY (ESTADO Y SEMÁFORO LADO A LADO)
# ==========================================
with tab_hoy:
    c_metrics, c_semaforo = st.columns([1.5, 1])
    
    with c_metrics:
        st.header("📊 Estatus")
        col1, col2, col3 = st.columns(3)
        col1.metric("HRV", f"{hrv_actual} ms")
        col2.metric("Body Battery", f"{body_battery}/100")
        col3.metric("Sueño", f"{sueno_puntuacion}/100")
        
    with c_semaforo:
        st.header("🚥 Predisposición")
        if hrv_actual < 40:
            st.markdown("<div class='semaforo-box semaforo-rojo'><b>🔴 ROJO</b><br>Fatiga SNC. Prioriza Z2 y recuperación activa. Evita fallo muscular.</div>", unsafe_allow_html=True)
        elif hrv_actual <= 45:
            st.markdown("<div class='semaforo-box semaforo-amarillo'><b>🟡 AMARILLO</b><br>Capacidad moderada. Entrena con control (RIR 2-3).</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='semaforo-box semaforo-verde'><b>🟢 VERDE</b><br>SNC Óptimo. Vía libre para cargas pesadas o alta intensidad.</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("🏋️‍♂️ Sesión Dinámica")
    disciplina = st.selectbox("Entrenamiento de hoy:", ["🏃‍♂️ Carrera / Trail", "🏋️‍♂️ Gimnasio", "🧗‍♂️ Escalada", "🧘‍♂️ Descanso Activo"], label_visibility="collapsed")
    
    if "Gimnasio" in disciplina:
        if hrv_actual < 40:
            st.info("**Fuerza Metabólica (3x15-20 reps / Bajo Peso)**\n\n1. Zancadas\n\n2. Flexiones\n\n3. Remo mancuerna")
        else:
            st.success("**Fuerza Máxima / Hipertrofia (4x5-10 reps / Alto Peso)**\n\n1. Sentadilla Barra\n\n2. Peso Muerto Rumano\n\n3. Dominadas Lastradas")
    elif "Carrera" in disciplina:
        if hrv_actual < 40: st.info("**Regenerativo. Z2 estricta (<148 ppm). Sin desnivel.**")
        else: st.success("**VO2 Max. Series o cuestas cortas (Z4/Z5).**")
    else: st.info("Movilidad, estiramientos o descanso total.")

# ==========================================
# PESTAÑA 2: AI COACH (CAJA FIJA ARRIBA + ORDEN INVERSO)
# ==========================================
with tab_chat:
    # Contenedor FIJO para la caja de escritura ARRIBA
    chat_input_container = st.container()
    
    # Contenedor para los mensajes (debajo de la caja de escritura)
    messages_container = st.container()
    
    # Inicialización del chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Mensaje de bienvenida inicial
        st.session_state.messages.append({"role": "assistant", "content": f"¡Hola Rodrigo! Tengo {len(archivos_subidos) if archivos_subidos else 0} archivos listos. Pídeme que los analice o hazme cualquier consulta deportiva."})
        
    # Mostramos los mensajes en el contenedor en orden INVERSO (el último arriba)
    with messages_container:
        # st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True) # Espacio para que no se pegue al input
        # Invertimos la lista de mensajes para mostrar
        for msg in reversed(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Lógica de input en el contenedor superior
    with chat_input_container:
        if prompt := st.chat_input("Escribe tu duda o reporta sensaciones...", key="chat_input"):
            # 1. Guardamos el mensaje del usuario (en orden normal para el historial lógico)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # 2. Mostramos el mensaje del usuario INMEDIATAMENTE
            # with messages_container: # No hace falta, al recargar saldrá arriba

            # 3. Lanzamos la petición de IA
            if api_configurada:
                try:
                    # Contexto multimodal (paquete de datos)
                    paquete_multimodal = [f"Rol: Entrenador deportivo de Rodrigo. Datos hoy: VFC:{hrv_actual}ms, BodyBattery:{body_battery}, Sueño:{sueno_puntuacion}. Consulta: {prompt}"]
                    
                    if archivos_subidos:
                        for archivo in archivos_subidos:
                            ext = archivo.name.split('.')[-1].lower()
                            if ext in ['jpg', 'jpeg', 'png']:
                                paquete_multimodal.append({"mime_type": f"image/{ext if ext != 'jpg' else 'jpeg'}", "data": archivo.getvalue()})
                            elif ext == 'csv':
                                try:
                                    archivo.seek(0)
                                    texto_csv = archivo.read().decode("utf-8")
                                    paquete_multimodal.append(f"\n[CSV: {archivo.name}]\n{texto_csv}")
                                except Exception: pass

                    # Usamos modelo 1.5-flash estable
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    respuesta_ia = model.generate_content(paquete_multimodal)
                    
                    # 4. Guardamos la respuesta de la IA
                    st.session_state.messages.append({"role": "assistant", "content": respuesta_ia.text})
                    
                except Exception as e:
                    st.session_state.messages.append({"role": "assistant", "content": f"Fallo de conexión: {str(e)}"})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "Configura la GOOGLE_API_KEY."})
            
            # Forzamos recarga para mover el nuevo mensaje arriba
            st.rerun()

# ==========================================
# PESTAÑA 3: ANALÍTICA (COMPACTA)
# ==========================================
with tab_historicos:
    st.header("📈 Base de Datos Analítica (52 Semanas)")
    
    fechas_anual = pd.date_range(end=datetime.date(2026, 6, 6), periods=52, freq='W')
    df_anual = pd.DataFrame({'Fecha': fechas_anual, 'HRV': np.random.randint(35, 60, size=52), 'Km': np.random.randint(15, 50, size=52), 'Carga_Aguda': np.random.randint(400, 800, size=52), 'Carga_Cronica': np.random.randint(450, 700, size=52)})

    st.subheader("1. Carga (Aguda vs Crónica)")
    fig_carga = go.Figure()
    fig_carga.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['Carga_Cronica'], fill='tozeroy', mode='none', name='Rango Óptimo', fillcolor='rgba(47, 133, 90, 0.4)'))
    fig_carga.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['Carga_Aguda'], mode='lines', name='Carga Actual', line=dict(color='#ff4b4b', width=2)))
    fig_carga.update_layout(template="plotly_dark", height=250, margin=dict(l=0,r=0,t=0,b=0), yaxis_title=None, legend=dict(orientation="h", y=1.1, x=0))
    st.plotly_chart(fig_carga, use_container_width=True)

    st.subheader("2. Evolución VFC Anual")
    fig_salud = px.line(df_anual, x='Fecha', y='HRV', color_discrete_sequence=['#ff4b4b'], template="plotly_dark")
    fig_salud.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), yaxis_title=None)
    st.plotly_chart(fig_salud, use_container_width=True)

# ==========================================
# PESTAÑA 4: PLANES (EN CONSTRUCCIÓN)
# ==========================================
with tab_planes:
    st.header("🗓️ Planificación Semanal / Mensual")
    st.write("Bloques de fuerza, carrera y focos estratégicos.")
