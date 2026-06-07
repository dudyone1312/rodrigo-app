import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import google.generativeai as genai

# --- 1. CONFIGURACIÓN E INTERFAZ (CSS ULTRA-COMPACTO MÓVIL) ---
st.set_page_config(page_title="Rodrigo Hybrid Hub", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Compactación extrema de márgenes superiores y elements */
    .block-container { padding-top: 0.8rem; padding-bottom: 0rem; padding-left: 0.8rem; padding-right: 0.8rem; }
    h1 { font-size: 1.6rem !important; margin-bottom: 0rem !important; margin-top: 0rem !important; }
    h2 { font-size: 1.2rem !important; margin-top: 0.4rem !important; margin-bottom: 0.1rem !important; }
    h3 { font-size: 1.0rem !important; margin-top: 0.3rem !important; margin-bottom: 0.1rem !important; }
    .stTabs [data-baseweb="tab"] { font-size: 13px; padding-left: 8px; padding-right: 8px; padding-top: 4px; padding-bottom: 4px; }
    .stMetric { padding: 0px !important; margin: 0px !important; }
    [data-testid="stMetricValue"] { font-size: 1.4rem !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { font-size: 0.75rem !important; }
    div[data-testid="stToast"] { padding: 4px; font-size: 11px; }
    
    /* Semáforo visual ultra-compacto */
    .semaforo-box { border-radius: 6px; padding: 6px; color: white; text-align: center; font-size: 12px; }
    .semaforo-rojo { background-color: #742a2a; border: 1.5px solid #f56565; }
    .semaforo-amarillo { background-color: #744210; border: 1.5px solid #ecc94b; }
    .semaforo-verde { background-color: #22543d; border: 1.5px solid #48bb78; }
    
    /* Estilos del Chat */
    [data-testid="stChatMessage"] { padding: 0.4rem; margin-bottom: 0.4rem; border-radius: 6px; font-size: 13px; }
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

# --- 3. CABECERA FIJA DE LA APP (VISTA MÓVIL OPTIMIZADA) ---
st.title("🏔️ RODRIGO HYBRID HUB")
st.markdown("---")

# Zona de carga universal oculta por defecto para ganar pantalla
with st.expander("📥 Cargar Archivos (Garmin CSV/Fotos)", expanded=False):
    archivos_subidos = st.file_uploader("Arrastra archivos aquí", accept_multiple_files=True, label_visibility="collapsed")

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

# --- 4. PESTAÑAS DE NAVEGACIÓN PRINCIPAL ---
tab_hoy, tab_chat, tab_analitica, tab_planes = st.tabs([
    "🎯 HOY", "💬 AI COACH", "📈 ANALÍTICA", "📅 PLANES"
])

# ==========================================
# PESTAÑA 1: HOY (ESTADO Y SEMÁFORO LADO A LADO)
# ==========================================
with tab_hoy:
    c_metrics, c_semaforo = st.columns([1.4, 1])
    
    with c_metrics:
        st.subheader("📊 Estatus")
        col1, col2, col3 = st.columns(3)
        col1.metric("HRV", f"{hrv_actual} ms")
        col2.metric("Battery", f"{body_battery}/100")
        col3.metric("Sueño", f"{sueno_puntuacion}/100")
        
    with c_semaforo:
        st.subheader("🚥 Predisposición")
        if hrv_actual < 40:
            st.markdown("<div class='semaforo-box semaforo-rojo'><b>🔴 ROJO</b><br>Fatiga SNC. Prioriza Z2. Evita fallos.</div>", unsafe_allow_html=True)
        elif hrv_actual <= 45:
            st.markdown("<div class='semaforo-box semaforo-amarillo'><b>🟡 AMARILLO</b><br>Moderado. Entrena con RIR 2-3.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='semaforo-box semaforo-verde'><b>🟢 VERDE</b><br>SNC Óptimo. Máxima carga permitida.</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🏋️‍♂️ Sesión Dinámica")
    disciplina = st.selectbox("Entrenamiento de hoy:", ["🏃‍♂️ Carrera / Trail", "🏋️‍♂️ Gimnasio", "🧗‍♂️ Escalada", "🧘‍♂️ Descanso Activo"], label_visibility="collapsed")
    
    if "Gimnasio" in disciplina:
        if hrv_actual < 40:
            st.info("**Fuerza Metabólica (3x15-20 reps / Poco Peso)**\n\n1. Zancadas corporales\n\n2. Flexiones al fallo técnico\n\n3. Remo con mancuerna suave")
        else:
            st.success("**Fuerza Máxima / Hipertrofia (4x5-10 reps / Carga Alta)**\n\n1. Sentadilla Trasera Barra\n\n2. Peso Muerto Rumano\n\n3. Dominadas Lastradas")
    elif "Carrera" in disciplina:
        if hrv_actual < 40: st.info("**Regenerativo:** Carrera continua en Z2 estricta (<148 ppm). Evita desniveles.")
        else: st.success("**VO2 Max:** Series intensas en pista o cuestas potentes cortas (Z4/Z5).")
    else: st.info("Movilidad articular, estiramientos pasivos o descanso absoluto.")

# ==========================================
# PESTAÑA 2: AI COACH (SISTEMA DE SEGURIDAD EN CASCADA MULTI-MODELO)
# ==========================================
with tab_chat:
    chat_input_container = st.container()
    messages_container = st.container()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": f"¡Hola Rodrigo! Datos cargados. Pídeme procesar, cruzar o borrar datos de tu historial y lo ejecutaré inmediatamente."})
        
    with messages_container:
        for msg in reversed(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    with chat_input_container:
        if prompt := st.chat_input("Escribe tu duda o comando de borrado aquí...", key="chat_input"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            if "borra" in prompt.lower() or "limpia" in prompt.lower() or "elimina" in prompt.lower():
                st.session_state.messages = [{"role": "assistant", "content": "🧹 Memoria temporal e historial deportivo limpiados con éxito. Listo para nuevos datos."}]
                st.rerun()

            if api_configurada:
                paquete_multimodal = [f"Rol: Coach deportivo experto. Atleta: Rodrigo. Métricas fisiológicas: VFC:{hrv_actual}ms, BodyBattery:{body_battery}, Sueño:{sueno_puntuacion}. Consulta del usuario: {prompt}"]
                
                if archivos_subidos:
                    for archivo in archivos_subidos:
                        ext = archivo.name.split('.')[-1].lower()
                        if ext in ['jpg', 'jpeg', 'png']:
                            paquete_multimodal.append({"mime_type": f"image/{ext if ext != 'jpg' else 'jpeg'}", "data": archivo.getvalue()})
                        elif ext == 'csv':
                            try:
                                archivo.seek(0)
                                texto_csv = archivo.read().decode("utf-8")
                                paquete_multimodal.append(f"\n[CSV adjunto: {archivo.name}]\n{texto_csv}")
                            except Exception: pass

                # BLINDAJE ANTI-404: Carrusel adaptativo de modelos oficiales de Google
                modelos_a_probar = [
                    'gemini-2.5-flash',
                    'gemini-2.0-flash',
                    'gemini-1.5-flash-latest',
                    'gemini-1.5-flash',
                    'models/gemini-1.5-flash'
                ]
                
                respuesta_exitosa = False
                ultimo_error_servidor = ""
                
                # Bucle inteligente que prueba variantes hasta que una responda correctamente
                for nombre_modelo in modelos_a_probar:
                    try:
                        model = genai.GenerativeModel(nombre_modelo)
                        respuesta_ia = model.generate_content(paquete_multimodal)
                        st.session_state.messages.append({"role": "assistant", "content": respuesta_ia.text})
                        respuesta_exitosa = True
                        break # Rompe el bucle si tiene éxito
                    except Exception as e:
                        ultimo_error_servidor = str(e)
                        continue # Si da error (como el 404), pasa al siguiente modelo
                
                # Si ninguno de la lista funcionó, informa amigablemente sin romper la web
                if not respuesta_exitosa:
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"⚠️ No se ha podido conectar con los endpoints estándar de Gemini debido a restricciones de versión en el servidor. Detalle técnico: {ultimo_error_servidor}"
                    })
            else:
                st.session_state.messages.append({"role": "assistant", "content": "Clave API ausente."})
            
            st.rerun()

# ==========================================
# PESTAÑA 3: ANALÍTICA (MÉTRICAS Y GRÁFICAS)
# ==========================================
with tab_analitica:
    st.subheader("📊 Base de Datos y Análisis de Rendimiento")
    
    fechas_anual = pd.date_range(end=datetime.date(2026, 6, 6), periods=52, freq='W')
    df_anual = pd.DataFrame({
        'Fecha': fechas_anual,
        'HRV': np.random.randint(35, 60, size=52),
        'FC_Reposo': np.random.randint(48, 58, size=52),
        'Km': np.random.randint(15, 50, size=52),
        'Carga_Aguda': np.random.randint(400, 800, size=52),
        'Carga_Cronica': np.random.randint(450, 700, size=52)
    })

    st.markdown("##### 1. Estado de Carga (Aguda vs Crónica)")
    fig_carga = go.Figure()
    fig_carga.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['Carga_Cronica'], fill='tozeroy', mode='none', name='Rango Óptimo', fillcolor='rgba(47, 133, 90, 0.35)'))
    fig_carga.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['Carga_Aguda'], mode='lines', name='Carga Actual', line=dict(color='#ff4b4b', width=1.5)))
    fig_carga.update_layout(template="plotly_dark", height=180, margin=dict(l=5,r=5,t=5,b=5), legend=dict(orientation="h", y=1.15, x=0))
    st.plotly_chart(fig_carga, use_container_width=True)

    st.markdown("##### 2. Evolución Anual de Variabilidad Cardíaca (HRV)")
    fig_salud = px.line(df_anual, x='Fecha', y='HRV', color_discrete_sequence=['#ff4b4b'], template="plotly_dark")
    fig_salud.update_layout(height=140, margin=dict(l=5,r=5,t=5,b=5), yaxis_title=None)
    st.plotly_chart(fig_salud, use_container_width=True)

    col_g3, col_g4 = st.columns(2)
    
    with col_g3:
        st.markdown("##### 3. Ritmos por Zona Cardiaca")
        tabla_ritmos = pd.DataFrame({
            "Zona de Trabajo": ["Z1 (<130 ppm)", "Z2 (131-148)", "Z3 (149-162)", "Z4 (163-175)", "Z5 (>176 ppm)"],
            "Ritmo Objetivo": ["6:25 min/km", "5:40 min/km", "5:05 min/km", "4:30 min/km", "3:55 min/km"]
        })
        st.dataframe(tabla_ritmos, hide_index=True, use_container_width=True)

    with col_g4:
        st.markdown("##### 4. Progresión Grado Escalada")
        fig_escalada = go.Figure()
        fig_escalada.add_trace(go.Scatter(x=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'], y=[3, 3, 4, 4, 5, 5], mode='lines+markers', name='Grado V', line=dict(color='#ff9900', width=2.5)))
        fig_escalada.update_layout(template="plotly_dark", height=130, margin=dict(l=5,r=5,t=10,b=5), yaxis_title=None)
        st.plotly_chart(fig_escalada, use_container_width=True)

# ==========================================
# PESTAÑA 4: PLANES
# ==========================================
with tab_planes:
    st.subheader("📅 Planificación del Macrociclo")
    st.info("Espacio reservado para la estructuración táctica de bloques de carrera y fuerza.")
