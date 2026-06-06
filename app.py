import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rodrigo Hybrid Hub", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Rodrigo Performance Hub")
st.subheader("Tu Portal de Rendimiento Híbrido & Trail")
st.markdown("---")

uploaded_file = st.file_uploader("📥 Arrastra aquí tu archivo CSV de Garmin (Actividades o Sueño)", type=["csv"])
st.markdown("---")

st.header("📊 Estatus del Atleta")
col1, col2, col3 = st.columns(3)

hrv_actual = 39
body_battery = 61
estado_recuperacion = "Precaución (SNC en recuperación)"

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if 'Puntuación' in df.columns:
            hrv_actual = int(df.iloc[0]['Estado de VFC'])
            body_battery = int(df.iloc[0]['Body Battery'])
            st.success("✅ CSV de Sueño procesado correctamente.")
        else:
            st.success("✅ CSV de Actividades cargado correctamente.")
    except Exception as e:
        st.error("Archivo cargado. Procesando estructura...")

with col1:
    st.metric(label="Variabilidad Cardíaca (HRV)", value=f"{hrv_actual} ms")
with col2:
    st.metric(label="Body Battery", value=f"{body_battery}/100")
with col3:
    st.markdown(f"**Estado Fisiológico:**\n\n{estado_recuperacion}")

st.markdown("---")
st.header("🏃‍♂️ Prescripción de la Sesión Diaria")

if hrv_actual < 40:
    st.warning("⚠️ Sistema Nervioso Central deprimido (VFC en 39 ms). Evitamos alta intensidad neuromuscular.")
    opcion_entreno = st.selectbox(
        "Elige la variante de entrenamiento que mejor se adapte a tus sensaciones de hoy:",
        ["Opción A: Trail / Ruteo por montaña (Z2 - Ritmo controlado - Serra de Tramuntana)", 
         "Opción B: Fuerza de Recondicionamiento (Metabólica - Series de 20 repeticiones)", 
         "Opción C: Descanso Activo / Movilidad y Flexibilidad Fluyida"]
    )
    
    st.markdown("### 📋 Estructura de la Sesión Seleccionada")
    if "Opción A" in opcion_entreno:
        st.write("🏃‍♂️ **Enfoque:** Resistencia base en entorno real. Senderismo rápido o trote suave en pendientes medias cerca de Palma. Limita los saltos e impactos bruscos en las bajadas.")
    elif "Opción B" in opcion_entreno:
        st.write("🏋️‍♂️ **Enfoque:** Buscamos capilarización y bombeo sin estrés pesado. Realiza 3-4 series de 20 repeticiones. Ejercicios: Zancadas caminando ligeras, flexiones controladas, remo con mancuerna y core.")
    else:
        st.write("🧘‍♂️ **Enfoque:** Regeneración pura. 30 minutos de transiciones de movilidad articular (gato-camello, aperturas de cadera) para acelerar la recuperación.")
else:
    st.success("✅ SNC Listo para recibir carga de alta intensidad.")
