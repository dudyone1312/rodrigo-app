import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import google.generativeai as genai
from PIL import Image  # Permite procesar capturas y fotos de forma real

# --- 1. CONFIGURACIÓN E INTERFAZ (CSS ULTRA-COMPACTO MÓVIL) ---
st.set_page_config(page_title="Rodrigo Hybrid Hub", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding-top: 0.8rem; padding-bottom: 0rem; padding-left: 0.8rem; padding-right: 0.8rem; }
    h1 { font-size: 1.6rem !important; margin-bottom: 0rem !important; margin-top: 0rem !important; }
    h2 { font-size: 1.2rem !important; margin-top: 0.4rem !important; margin-bottom: 0.1rem !important; }
    h3 { font-size: 1.0rem !important; margin-top: 0.3rem !important; margin-bottom: 0.1rem !important; }
    .stTabs [data-baseweb="tab"] { font-size: 13px; padding-left: 8px; padding-right: 8px; padding-top: 4px; padding-bottom: 4px; }
    .stMetric { padding: 0px !important; margin: 0px !important; }
    [data-testid="stMetricValue"] { font-size: 1.4rem !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { font-size: 0.75rem !important; }
    div[data-testid="stToast"] { padding: 4px; font-size: 11px; }
    
    .semaforo-box { border-radius: 6px; padding: 6px; color: white; text-align: center; font-size: 12px; }
    .semaforo-rojo { background-color: #742a2a; border: 1.5px solid #f56565; }
    .semaforo-amarillo { background-color: #744210; border: 1.5px solid #ecc94b; }
    .semaforo-verde { background-color: #22543d; border: 1.5px solid #48bb78; }
    
    [data-testid="stChatMessage"] { padding: 0.4rem; margin-bottom: 0.4rem; border-radius: 6px; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURACIÓN DE LA API (DOBLE COMPROBACIÓN ADAPTATIVA) ---
api_configurada = False
clave_encontrada = None

if "GOOGLE_API_KEY" in st.secrets:
    clave_encontrada = st.secrets["GOOGLE_API_KEY"]
elif "GOOGLE API KEY" in st.secrets:
    clave_encontrada = st.secrets["GOOGLE API KEY"]

if clave_encontrada:
    try:
        genai.configure(api_key=clave_encontrada)
        api_configurada = True
    except Exception as e:
        st.sidebar.error(f"Error en credenciales: {e}")

# --- 3. CABECERA Y ENTRADA DE DATOS MULTI-FORMATO ---
st.title("🏔️ RODRIGO HYBRID HUB")
st.markdown("---")

with st.expander("📥 Cargar Archivos (Garmin CSV/Fotos)", expanded=False):
    archivos_subidos = st.file_uploader("Arrastra archivos aquí", accept_multiple_files=True, label_visibility="collapsed")

# Biométricos base por defecto
hrv_actual = 39
body_battery = 61
sueno_puntuacion = 86
datos_csv_contexto = ""
lista_imagenes_pil = []

# Procesamiento adaptativo según el tipo de archivo subido
if archivos_subidos:
    for archivo in archivos_subidos:
        extension = archivo.name.split('.')[-1].lower()
        
        # Si es un archivo de datos (CSV)
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
                
                datos_csv_contexto += f"\n[Datos extraídos del CSV {archivo.name}]:\n{df.head(10).to_string()}\n"
            except Exception:
                pass
                
        # Si es una imagen (Captura de pantalla, PNG, JPG, etc.)
        elif extension in ['png', 'jpg', 'jpeg', 'webp']:
            try:
                archivo.seek(0)
                img_abierta = Image.open(archivo)
                lista_imagenes_pil.append(img_abierta)
                st.toast(f"📸 Imagen vinculada al Coach: {archivo.name}", icon="🖼️")
            except Exception:
                pass

# --- 4. PESTAÑAS DE NAVEGACIÓN ---
tab_hoy, tab_chat, tab_analitica, tab_planes = st.tabs(["🎯 HOY", "💬 AI COACH", "📈 ANALÍTICA", "📅 PLANES"])

# PESTAÑA 1: HOY
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
        if hrv_actual < 40: st.info("**Fuerza Metabólica (3x15-20 reps)**\n\n1. Zancadas corporales\n2. Flexiones al fallo técnico\n3. Remo suave")
        else: st.success("**Fuerza Máxima (4x5-10 reps)**\n\n1. Sentadilla Trasera\n2. Peso Muerto\n3. Dominadas Lastradas")
    elif "Carrera" in disciplina:
        if hrv_actual < 40: st.info("**Regenerativo:** Carrera continua en Z2 estricta (<148 ppm).")
        else: st.success("**VO2 Max:** Series intensas en pista o cuestas (Z4/Z5).")
    else: st.info("Movilidad articular o descanso absoluto.")

# PESTAÑA 2: AI COACH (ENTORNO MULTIMODAL DIRECTO DE ALTA DISPONIBILIDAD)
with tab_chat:
    chat_input_container = st.container()
    messages_container = st.container()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "¡Hola Rodrigo! Conexión adaptativa activada. Puedes escribirme, subir tus planificaciones en CSV o arrastrar directamente capturas de pantalla de tus métricas de Garmin para que las analicemos juntos."})
        
    with messages_container:
        for msg in reversed(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    with chat_input_container:
        if prompt := st.chat_input("Solicita tu entreno o analiza tus archivos aquí...", key="chat_input"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            if any(x in prompt.lower() for x in ["borra", "limpia", "elimina"]):
                st.session_state.messages = [{"role": "assistant", "content": "🧹 Historial de chat y memoria reseteados."}]
                st.rerun()

            if api_configurada:
                try:
                    # DESCUBRIMIENTO EVOLUTIVO: Busca modelos activos válidos omitiendo versiones obsoletas
                    modelos_validos = []
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            modelos_validos.append(m.name)
                    
                    # Selecciona prioritariamente el canal Flash que esté operativo en 2026
                    modelos_flash = [m for m in modelos_validos if "flash" in m.lower()]
                    modelo_final = modelos_flash[0] if modelos_flash else (modelos_validos[0] if modelos_validos else 'gemini-2.0-flash')
                    
                    # Construcción del contexto textual estructurado
                    contexto_instruccion = (
                        f"Rol: Eres el Coach deportivo experto y entrenador personal de Rodrigo.\n"
                        f"Métricas del día: HRV/VFC: {hrv_actual}ms, Body Battery: {body_battery}%, Sueño: {sueno_puntuacion}/100.\n"
                        f"{datos_csv_contexto}\n"
                        f"Instrucción actual de Rodrigo: {prompt}\n"
                        f"Nota: Si hay imágenes adjuntas en el paquete, analízalas detalladamente ya que contienen sus datos de rendimiento."
                    )
                    
                    # Empaquetado multimodal (Texto del prompt + Objetos de imagen reales de Pillow)
                    paquete_peticion = [contexto_instruccion]
                    for img in lista_imagenes_pil:
                        paquete_peticion.append(img)
                    
                    # Generación de la respuesta inteligente
                    model = genai.GenerativeModel(modelo_final)
                    resp = model.generate_content(paquete_peticion)
                    st.session_state.messages.append({"role": "assistant", "content": resp.text})
                    
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        st.session_state.messages.append({"role": "assistant", "content": "🛑 **Aviso de Cuota:** Hemos alcanzado las peticiones gratuitas máximas por hora que concede Google. El código y el canal están perfectos, la cuota se reiniciará automáticamente en un momento."})
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Error en el procesamiento del modelo: {e}"})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "❌ **Falta API Key:** Por favor, asegúrate de añadir la variable `GOOGLE_API_KEY` en la sección Advanced Settings -> Secrets de tu panel de Streamlit Cloud."})
            
            st.rerun()

# PESTAÑA 3: ANALÍTICA
with tab_analitica:
    st.subheader("📊 Base de Datos y Análisis de Rendimiento")
    fechas_anual = pd.date_range(end=datetime.date(2026, 6, 6), periods=52, freq='W')
    df_anual = pd.DataFrame({
        'Fecha': fechas_anual, 'HRV': np.random.randint(35, 60, size=52),
        'Carga_Aguda': np.random.randint(400, 800, size=52), 'Carga_Cronica': np.random.randint(450, 700, size=52)
    })
    
    st.markdown("##### 1. Estado de Carga (Aguda vs Crónica)")
    fig_carga = go.Figure()
    fig_carga.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['Carga_Cronica'], fill='tozeroy', mode='none', name='Rango Óptimo', fillcolor='rgba(47, 133, 90, 0.35)'))
    fig_carga.add_trace(go.Scatter(x=df_anual['Fecha'], y=df_anual['Carga_Aguda'], mode='lines', name='Carga Actual', line=dict(color='#ff4b4b', width=1.5)))
    fig_carga.update_layout(template="plotly_dark", height=180, margin=dict(l=5,r=5,t=5,b=5), legend=dict(orientation="h", y=1.15, x=0))
    st.plotly_chart(fig_carga, use_container_width=True)

# PESTAÑA 4: PLANES
with tab_planes:
    st.subheader("📅 Planificación del Macrociclo")
    st.info("Espacio reservado para la estructuración táctica de bloques de carrera y fuerza.")
