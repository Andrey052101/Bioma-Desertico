import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 🛠️ Configuración de la página
st.set_page_config(page_title="🌵 Ecosistema Desértico", layout="wide")

# 📂 Ruta base relativa (compatible con Streamlit Cloud)
ruta_base = os.path.dirname(__file__)

# 📸 Mostrar imágenes decorativas
st.image(os.path.join(ruta_base, "minecraf.jpg"), caption="Bioma Desértico en Minecraft", use_column_width=True)
st.image(os.path.join(ruta_base, "cadena alimenticia.png"), caption="Cadena Alimenticia del Ecosistema", use_column_width=True)

# 📥 Cargar datos desde el archivo Excel
archivo = os.path.join(ruta_base, "simulacion_desertica.xlsx")

@st.cache_data
def cargar_datos():
    condiciones = pd.read_excel(archivo, sheet_name="Condiciones Ambientales")
    fauna = pd.read_excel(archivo, sheet_name="Fauna")
    flora = pd.read_excel(archivo, sheet_name="Flora")
    eventos = pd.read_excel(archivo, sheet_name="Eventos")
    indicadores = pd.read_excel(archivo, sheet_name="Indicadores de Equilibrio")
    return condiciones, fauna, flora, eventos, indicadores

condiciones, fauna, flora, eventos, indicadores = cargar_datos()

# 🧭 Navegación por pestañas
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌡️ Ambiente", "🐾 Fauna", "🌵 Flora", "🌪️ Eventos", "📊 Equilibrio"])

# 🌡️ Condiciones Ambientales
with tab1:
    st.subheader("Condiciones Ambientales")
    condiciones["Diferencia"] = condiciones["Valor Final"] - condiciones["Valor Inicial"]
    condiciones["Cambio (%)"] = ((condiciones["Diferencia"] / condiciones["Valor Inicial"]) * 100).round(2)
    st.dataframe(condiciones)

    fig = px.bar(condiciones, x="Variable", y=["Valor Inicial", "Valor Final"], barmode="group",
                 title="Comparación de Condiciones Ambientales", color_discrete_sequence=["skyblue", "orange"])
    st.plotly_chart(fig)

# 🐾 Fauna
with tab2:
    st.subheader("Poblaciones de Fauna")
    fauna["Diferencia"] = fauna["Cantidad Final"] - fauna["Cantidad Inicial"]
    fauna["Cambio (%)"] = ((fauna["Diferencia"] / fauna["Cantidad Inicial"]) * 100).round(2)
    st.dataframe(fauna)

    for _, row in fauna.iterrows():
        st.metric(label=row["Especie"], value=row["Cantidad Final"], delta=f"{row['Diferencia']} desde inicio")

    fig = px.bar(fauna, x="Especie", y=["Cantidad Inicial", "Cantidad Final"], barmode="group",
                 title="Comparación de Fauna", color_discrete_sequence=["lightgreen", "darkgreen"])
    st.plotly_chart(fig)

# 🌵 Flora
with tab3:
    st.subheader("Vegetación del Bioma")
    st.dataframe(flora)

    fig = px.bar(flora, x="Planta", y="Cantidad", color="Tipo", title="Distribución de Flora")
    st.plotly_chart(fig)

# 🌪️ Eventos Naturales
with tab4:
    st.subheader("Eventos Naturales Registrados")
    st.dataframe(eventos)

# 📊 Indicadores de Equilibrio
with tab5:
    st.subheader("Indicadores de Equilibrio")
    indicadores["Diferencia"] = indicadores["Valor Final"] - indicadores["Valor Inicial"]
    indicadores["Cambio (%)"] = ((indicadores["Diferencia"] / indicadores["Valor Inicial"]) * 100).round(2)
    st.dataframe(indicadores)

    categoria = st.selectbox("Selecciona una categoría", indicadores["Categoria"].unique())
    filtro = indicadores[indicadores["Categoria"] == categoria]

    fig = px.bar(filtro, x="Mobs", y=["Valor Inicial", "Valor Final"], barmode="group",
                 title=f"Indicadores de {categoria}", color_discrete_sequence=["skyblue", "orange"])
    st.plotly_chart(fig)
