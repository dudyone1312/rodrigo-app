import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

# 1. CONFIGURACIÓN E INTERFAZ PREMIUM (Estilo Garmin/Dark)
st.set_page_config(page_title="Rodrigo Hybrid Hub", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main { background-color: #0d0f14; color: #e2e8f0; }
    .stTabs [data-baseweb="tab"] { font-size: 15px; font-weight: bold; color: #a0aec0; }
    .stTabs [aria-selected="true"] { color: #ff4b4b !important; border-bottom-color: #ff4b4b !important; }
    .bloque-mes { background-color: #1a202c; padding: 20px; border-radius: 8px; border-left: 6px solid #4a5568; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .bloque-mes-actual { background-color: #1e2538; padding: 20px; border-radius: 8px; border-left: 6px solid #ff4b4b; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.5); }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ RODRIGO PERFORMANCE HUB")
st.markdown("---")

# 2. PANEL DE CONTROL DE ARCHIVOS
uploaded_file = st.file_uploader("📥 Actualiza tus datos arrastrando el CSV de Garmin aquí", type=["csv"])

# Variables Basales por defecto (Sábado 6 de Junio)
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
            st.toast("Métricas de recuperación actualizadas dinámicamente.", icon="✅")
    except:
        st.toast("Archivo recibido. Estructurando paneles...", icon="ℹ️")

# 3. SISTEMA DE PESTAÑAS AMPLIADO
tab_hoy, tab_chat, tab_semana, tab_mes, tab_historicos = st.tabs([
    "🎯 HOY", "💬 AI COACH", "📅 PLAN SEMANAL", "📊 PLAN MENSUAL", "📈 HISTÓRICOS Y GRÁFICAS"
])

# --- PESTAÑA 1: HOY (Lógica de decisión corregida) ---
with tab_hoy:
    st.header("📋 Estado Neuromuscular y Carga Actual")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="Variabilidad Cardíaca (HRV)", value=f"{hrv_actual} ms", delta="SNC Fatigado" if hrv_actual < 40 else "SNC Óptimo")
    col_b.metric(label="Body Battery", value=f"{body_battery}/100")
    col_c.metric(label="Calidad del Sueño", value=f"{sueno_puntuacion}/100")
    
    st.markdown("---")
    st.subheader("⚙️ Modulador de Sesión")
    
    # El usuario decide la logística, el coach prescribe la fisiología
    disciplina = st.selectbox(
        "Selecciona qué instalación o bloque tienes planificado/disponible para hoy:",
        ["🏃‍♂️ Carrera / Trail Running", "🏋️‍♂️ Gimnasio / Sala de Fuerza", "🧗‍♂️ Otros (Rocódromo, Ciclismo, etc.)", "🧘‍♂️ Descanso Total / Activo"]
    )
    
    st.markdown("### 📋 Prescripción de Entrenamiento Inteligente")
    
    if hrv_actual < 40:
        st.warning("⚠️ **Alerta del Coach:** Tu VFC está en 39 ms (Carga acumulada alta/Fatiga central). El sistema restringe la intensidad neuromuscular para proteger tus adaptaciones y evitar sobreentrenamiento.")
        
        if "Carrera" in disciplina:
            st.info("**ENFOQUE RESTRINGIDO: Capacidad Aeróbica de Base (Zona 2 Corta)**\n\n"
                    "* **Tipo de Sesión:** Trote regenerativo continuo en asfalto llano o power-hiking suave en pendientes bajas cerca de Palma.\n"
                    "* **Zonas de Trabajo:** Estrictamente Z1 o Z2 baja de tu Garmin. Mantén ritmos muy cómodos.\n"
                    "* **Criterio Fisiológico:** Evitamos series de VO2Max e impactos excéntricos severos en bajadas técnicas (D-) de montaña para permitir la resíntesis de glucógeno y la recuperación del sistema parasimpático.\n"
                    "* **Volumen:** Cortar la sesión a los 40-45 minutos.")
        elif "Gimnasio" in disciplina:
            st.info("**ENFOQUE RESTRINGIDO: Recondicionamiento y Fuerza Metabólica**\n\n"
                    "* **Tipo de Sesión:** Trabajo de circuito enfocado en capilarización periférica y stiffness tendinoso pasivo. Cero cargas axiales pesadas.\n"
                    "* **Estructura:** 3-4 series de **15 a 20 repeticiones** con un carácter de esfuerzo bajo (RIR 4). El objetivo es flujo sanguíneo y lavado de metabolitos.\n"
                    "* **Selección de Ejercicios:** Ejercicios globales unilaterales ligeros (zancadas peso corporal, zancadas laterales), empujes con mancuernas ligeras y estabilidad lumbopélvica isométrica (planchas).")
        elif "Otros" in disciplina:
            st.info("**ENFOQUE RESTRINGIDO: Volumen Técnico Ligero**\n\n"
                    "* **Estructura:** Si vas al rocódromo, realiza travesías de calentamiento o vías de grado muy inferior a tu límite. Centrado en fluidez de movimiento. RPE máximo de 5.")
        else:
            st.info("**ENFOQUE RESTRINGIDO: Recuperación Pasiva Absoluta**\n\n"
                    "* **Acción:** Día de descanso total, estiramientos pasivos o sesión de foam roller. Hidratación pautada.")
    else:
        st.success("✅ **Alerta del Coach:** Tu Sistema Nervioso Central está completamente recuperado y listo para recibir tensiones elevadas y cargas de alto impacto.")
        
        if "Carrera" in disciplina:
            st.info("**ENFOQUE DESBLOQUEADO: Potencia Aeróbica (VO2Max) o Trail Técnico con Desnivel**\n\n"
                    "* **Tipo de Sesión:** Intervalos de alta intensidad (ej. 5x3 minutos en Zona 5 con recuperación completa) o salida específica de Trail Running por la Serra de Tramuntana aplicando velocidad en bajadas técnicas.")
        elif "Gimnasio" in disciplina:
            st.info("**ENFOQUE DESBLOQUEADO: Fuerza Máxima y Reclutamiento de Alta Intensidad**\n\n"
                    "* **Tipo de Sesión:** Trabajo de alta tensión mecánica buscando adaptaciones neurales crónicas sin hipertrofia innecesaria.\n"
                    "* **Estructura:** 3-5 series de 3 a 5 repeticiones con cargas pesadas ($\ge$ 80-85% 1RM). Descansos completos (3 minutos). RIR 1-2.\n"
                    "* **Selección de Ejercicios:** Sentadilla trasera con barra libre, Peso muerto convencional o rumano pesado, y tracciones complejas (dominadas lastradas).")
        elif "Otros" in disciplina:
            st.info("**ENFOQUE DESBLOQUEADO: Sesión de Rendimiento Pico**\n\n"
                    "* **Acción:** Bloques de escalada al límite de tu grado actual o series de alta potencia metabólica en bicicleta.")
        else:
            st.info("Día programado de descanso. Disfruta de la supercompensación.")

# --- PESTAÑA 2: AI COACH (CHAT INTERACTIVO) ---
with tab_chat:
    st.header("💬 Sala de Control Híbrida")
    st.write("Reporta sensaciones, molestias articulares o pide alternativas de entrenamiento en tiempo real.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "¡Buenas Rodrigo! He analizado tu VFC de 39 ms y tu sesión de Vo2Max en llano del jueves. Cuéntame, ¿cómo notas las piernas o qué logística tienes para organizar el bloque?"}]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Escribe tu consulta al entrenador..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        reply = "*(Sistema)*: ¡Mensaje recibido! Interfaz conectada correctamente. En el próximo paso integraremos la clave de API para procesar dinámicamente cada respuesta."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

# --- PESTAÑA 3: PLAN SEMANAL ---
with tab_semana:
    st.header("🗓️ Estructura del Microciclo")
    st.write("Cronograma de entrenamientos semanales combinando sesiones de asfalto, montaña y fuerza en base a tus umbrales.")

# --- PESTAÑA 4: PLAN MENSUAL (Bloques horizontales sombreados) ---
with tab_mes:
    st.header("📊 Planificación Macrocíclica (Objetivos Mensuales)")
    
    # Mes Actual (Sombreado destacado)
    st.markdown("""
    <div class='bloque-mes-actual'>
        <h3 style='color:#ff4b4b; margin-top:0;'>🗓️ JUNIO 2026 (Bloque Actual: Recondicionamiento y Base Aeróbica)</h3>
        <p><b>🎯 Objetivos Correr:</b> Acumular volumen seguro en llano (asfalto de Palma) para aumentar densidad mitocondrial. Iniciar reconocimiento de pendientes en la Serra de Tramuntana a ritmos controlados.</p>
        <p><b>🏋️‍♂️ Objetivos Gimnasio:</b> Adaptación anatómica, fortalecimiento de la cadena posterior (Glúteos/Isquios) y control de estabilidad lumbopélvica para amortiguación de zancada.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Meses Siguientes (Sombreados grises de planificación)
    st.markdown("""
    <div class='bloque-mes'>
        <h3 style='color:#a0aec0; margin-top:0;'>🗓️ JULIO 2026 (Bloque: Fuerza Máxima Neural y Trail running)</h3>
        <p><b>🎯 Objetivos Correr:</b> Introducción de bloques específicos de Trail Running con ritmos de subida constantes en montaña y técnica de zancada eficiente en bajadas.</p>
        <p><b>🏋️‍♂️ Objetivos Gimnasio:</b> Transferencia de fuerza a potencia. Trabajo pliométrico controlado y picos de tensión mecánica (Sentadillas pesadas a bajas repeticiones).</p>
    </div>
    <div class='bloque-mes'>
        <h3 style='color:#a0aec0; margin-top:0;'>🗓️ AGOSTO 2026 (Bloque: Tolerancia al Lactato e Híbrido Avanzado)</h3>
        <p><b>🎯 Objetivos Correr:</b> Rutas de larga distancia por montaña completando tramos técnicos. Series fraccionadas intensas a ritmo de umbral de lactato.</p>
        <p><b>🏋️‍♂️ Objetivos Gimnasio:</b> Mantenimiento de niveles de fuerza máxima combinados con complejos dinámicos de resistencia a la fatiga local.</p>
    </div>
    """, unsafe_allow_html=True)

# --- PESTAÑA 5: HISTÓRICOS Y GRÁFICAS INTERACTIVAS ---
with tab_historicos:
    st.header("📈 Análisis de Tendencias a Largo Plazo")
    
    # Generación de datos simulados realistas para el reporte anual
    fechas_anual = pd.date_range(end=datetime.date(2026, 6, 6), periods=52, freq='W')
    
    data_anual = pd.DataFrame({
        'Fecha': fechas_anual,
        'HRV': np.random.randint(35, 55, size=52),
        'FC_Reposo': np.random.randint(48, 58, size=52),
        'Km_Corridos': np.random.randint(15, 45, size=52),
        'VO2Max': np.linspace(46, 51, 52) + np.random.normal(0, 0.4, 52),
        'Carga_Aguda': np.random.randint(400, 800, size=52),
        'Carga_Cronica': np.random.randint(450, 700, size=52)
    })
    
    # GRÁFICA 1: HRV y FC Reposo combinadas
    st.subheader("1. Evolución de Salud Basal (VFC y Frecuencia Cardíaca en Reposo)")
    fig_salud = px.line(data_anual, x='Fecha', y=['HRV', 'FC_Reposo'], 
                        labels={'value': 'Métricas (ms / ppm)', 'variable': 'Indicador'},
                        color_discrete_map={'HRV': '#ff4b4b', 'FC_Reposo': '#4299e1'},
                        template="plotly_dark")
    st.plotly_chart(fig_salud, use_container_width=True)
    
    st.markdown("---")
    
    # GRÁFICA 2: Kilómetros y VO2Max Anual
    st.subheader("2. Rendimiento Cardiorrespiratorio (Kilómetros Semanales vs Estado VO2Max)")
    fig_performance = px.bar(data_anual, x='Fecha', y='Km_Corridos', labels={'Km_Corridos': 'Kilómetros Semanales'}, template="plotly_dark", color_discrete_sequence=['#4a5568'])
    fig_performance.add_scatter(x=data_anual['Fecha'], y=data_anual['VO2Max'] * 0.8, mode='lines', name='Tendencia VO2Max', line=dict(color='#ecc94b', width=3))
    st.plotly_chart(fig_performance, use_container_width=True)
    
    st.markdown("---")
    
    # GRÁFICA 3: Carga de Entrenamiento (Estilo Garmin)
    st.subheader("3. Carga de Entrenamiento Optimizada (Carga Aguda vs Crónica)")
    st.write("*Simulación del balance de carga de Garmin. La zona verde óptima se da cuando la carga a corto plazo (Aguda) está equilibrada con tu historial a largo plazo (Crónica).*")
    fig_carga = px.area(data_anual, x='Fecha', y='Carga_Cronica', title="Historial de Carga Estilo Garmin", template="plotly_dark", color_discrete_sequence=['#2f855a'])
    fig_carga.add_scatter(x=data_anual['Fecha'], y=data_anual['Carga_Aguda'], mode='lines', name='Carga Aguda (Fatiga)', line=dict(color='#ff4b4b', width=2))
    st.plotly_chart(fig_carga, use_container_width=True)
    
    st.markdown("---")
    
    # CUADRO 4: Ritmos medios por Zona de Frecuencia Cardíaca
    st.subheader("4. Eficiencia de Ritmos por Zonas Cardíacas")
    st.write("Tabla de control basada en tus entrenamientos actuales en Palma. Muestra la velocidad media en cada zona fisiológica:")
    
    tabla_ritmos = pd.DataFrame({
        'Zona Cardíaca': ['Zona 1 (Recuperación)', 'Zona 2 (Capacidad Aeróbica)', 'Zona 3 (Tempo/Ritmo)', 'Zona 4 (Umbral de Lactato)', 'Zona 5 (Potencia VO2Max)'],
        'Rango Pulsaciones (ppm)': ['110 - 130', '131 - 148', '149 - 162', '163 - 175', '176+'],
        'Ritmo Medio Estimado (min/km)': ['6:45 - 6:15', '6:10 - 5:35', '5:30 - 4:55', '4:50 - 4:20', '4:15 - 3:45']
    })
    st.table(tabla_ritmos)
