import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import google.generativeai as genai

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS UI
# ==========================================
st.set_page_config(
    page_title="Rodrigo Performance Hub",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Optimización estética para móviles y visualización compacta
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stButton>button { width: 100%; border-radius: 10px; }
    .chat-bubble { padding: 10px; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_style=False)

# ==========================================
# 2. CONEXIÓN SEGURA CON GEMINI (ANTI-404)
# ==========================================
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ No se ha encontrado la clave 'GOOGLE_API_KEY' en los Secrets de Streamlit. Por favor, añádela en la configuración de tu panel de Streamlit Cloud.")

def obtener_modelo_gemini():
    """Busca dinámicamente un modelo disponible para evitar el Error 404."""
    try:
        modelos = [m.name for m in genai.list_models() if "gemini-1.5-flash" in m.name]
        return modelos[0] if modelos else "gemini-1.5-flash"
    except Exception:
        return "gemini-1.5-flash"

# ==========================================
# 3. INICIALIZACIÓN DEL ESTADO DE LA APP (PERSISTENCIA TEMPORAL)
# ==========================================
if "mensajes_chat" not in st.session_state:
    st.session_state.mensajes_chat = [
        {"role": "assistant", "content": "¡Hola! Soy tu coach de IA. ¿Qué aspecto de tu entrenamiento o salud vamos a revisar hoy?"}
    ]

if "historico_salud" not in st.session_state:
    # Datos iniciales de ejemplo para que la gráfica no aparezca vacía
    st.session_state.historico_salud = pd.DataFrame([
        {"Fecha": "2026-06-01", "Peso (kg)": 78.5, "Sueño (hrs)": 7.5, "Energía (1-10)": 8},
        {"Fecha": "2026-06-04", "Peso (kg)": 78.1, "Sueño (hrs)": 6.8, "Energía (1-10)": 7}
    ])

if "planificaciones" not in st.session_state:
    st.session_state.planificaciones = "Aún no has generado ninguna planificación para esta semana. Ve a la pestaña de IA para crear una basada en tus datos actuales."

# ==========================================
# 4. ESTRUCTURA DE LA INTERFAZ DE USUARIO
# ==========================================
st.title("🚀 Rodrigo Performance Hub")
st.caption("Tu ecosistema híbrido de rendimiento, salud y planificación inteligente.")

# Creación de pestañas para organizar la experiencia de usuario
tab_salud, tab_plan, tab_chat = st.tabs([
    "📊 Datos de Salud y Progreso", 
    "📅 Planificación y Entrenamientos", 
    "💬 Chat con Coach Gemini"
])

# ------------------------------------------
# PESTAÑA 1: DATOS DE SALUD Y PROGRESO
# ------------------------------------------
with tab_salud:
    st.header("Formulario de Registro Biométrico")
    
    # Crear dos columnas para optimizar el espacio en pantallas grandes
    col1, col2 = st.columns(2)
    
    with col1:
        fecha_registro = st.date_input("Fecha del registro", datetime.date.today())
        peso = st.number_input("Peso Corporal (kg)", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
    
    with col2:
        horas_sueno = st.slider("Horas de Sueño", min_value=0.0, max_value=16.0, value=7.0, step=0.5)
        nivel_energia = st.slider("Nivel de Energía General (1 al 10)", min_value=1, max_value=10, value=7)
        
    if st.button("Guardar Registro del Día"):
        nuevo_registro = {
            "Fecha": str(fecha_registro),
            "Peso (kg)": peso,
            "Sueño (hrs)": horas_sueno,
            "Energía (1-10)": nivel_energia
        }
        # Añadir al registro histórico en memoria
        st.session_state.historico_salud = pd.concat([
            st.session_state.historico_salud, 
            pd.DataFrame([nuevo_registro])
        ], ignore_index=True)
        st.success("¡Datos guardados con éxito en la sesión actual!")

    st.write("---")
    st.subheader("Evolución de tus Métricas")
    
    # Mostrar tabla y gráfica interactiva si hay datos
    if not st.session_state.historico_salud.empty:
        st.dataframe(st.session_state.historico_salud, use_container_width=True)
        
        # Gráfica de evolución del peso utilizando Plotly
        fig_peso = px.line(
            st.session_state.historico_salud, 
            x="Fecha", 
            y="Peso (kg)", 
            title="Evolución del Peso Corporal",
            markers=True
        )
        st.plotly_chart(fig_peso, use_container_width=True)
    else:
        st.info("No hay datos históricos disponibles todavía.")

# ------------------------------------------
# PESTAÑA 2: PLANIFICACIÓN Y ENTRENAMIENTOS
# ------------------------------------------
with tab_plan:
    st.header("Tu Planificación Activa")
    st.info("Esta sección muestra los entrenamientos generados de forma personalizada por la Inteligencia Artificial.")
    
    # Caja de texto editable que mantiene la rutina actual
    rutina_actual = st.text_area(
        label="Rutina Semanal y Notas del Entrenador",
        value=st.session_state.planificaciones,
        height=350
    )
    st.session_state.planificaciones = rutina_actual
    
    if st.button("Guardar Modificaciones Manuales"):
        st.success("Planificación actualizada y guardada correctamente.")

# ------------------------------------------
# PESTAÑA 3: CHAT CON COACH GEMINI
# ------------------------------------------
with tab_chat:
    st.header("Estrategia e Inteligencia Artificial")
    st.caption("Pregúntale a Gemini sobre tus rutinas, pídele que analice tus datos de salud o que te diseñe un nuevo bloque de entrenamiento.")

    # Mostrar el historial de conversación en orden cronológico inverso
    for msg in st.session_state.mensajes_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Entrada de texto del usuario
    if prompt := st.chat_input("Escribe aquí tu duda (Ej: 'Genera un entrenamiento de pierna basado en mi nivel de energía de hoy')"):
        
        # Insertar mensaje del usuario en la pantalla inmediatamente
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.mensajes_chat.append({"role": "user", "content": prompt})
        
        # Procesar la petición con la API de Google de forma segura
        with st.spinner("Pensando como tu coach deportivo..."):
            try:
                modelo_disponible = obtener_modelo_gemini()
                model = genai.GenerativeModel(modelo_disponible)
                
                # Contextualizamos a la IA añadiendo los últimos datos de salud si existen
                contexto_salud = ""
                if not st.session_state.historico_salud.empty:
                    ultimo_registro = st.session_state.historico_salud.iloc[-1].to_dict()
                    contexto_salud = f"Datos actuales del atleta: {ultimo_registro}. "
                
                instruccion_sistema = (
                    f"Actúa como un Entrenador Personal de Élite y Experto en Ciencias del Deporte. "
                    f"{contexto_salud}Responde de forma clara, motivadora y estructurada en formato Markdown. "
                    f"Pregunta del usuario: {prompt}"
                )
                
                respuesta = model.generate_content(instruccion_sistema)
                texto_respuesta = respuesta.text
                
                # Mostrar respuesta en pantalla e incorporar al historial
                with st.chat_message("assistant"):
                    st.write(texto_respuesta)
                st.session_state.mensajes_chat.append({"role": "assistant", "content": texto_respuesta})
                
                # Si el usuario pidió explícitamente un entrenamiento o plan, lo sugerimos también en la pestaña de planes
                if "entrenamiento" in prompt.lower() or "planificación" in prompt.lower() or "rutina" in prompt.lower():
                    st.session_state.planificaciones = texto_respuesta
                    st.info("💡 He detectado una rutina en la respuesta. ¡También la he copiado automáticamente en tu pestaña de 'Planificación'!")
                    
            except Exception as e:
                st.error(f"Hubo un contratiempo al conectar con Gemini: {e}")
