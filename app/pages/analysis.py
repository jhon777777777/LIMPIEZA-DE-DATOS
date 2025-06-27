# app/pages/analysis.py

import streamlit as st
from app.utils.data_analyzer import analizar_dataframe
from app.visualization.dashboard import display_analysis_dashboard

# ✅ Agregar importaciones para usar el diccionario
from app.utils.labels_base import obtener_descripcion, generar_tabla_frecuencias

def display(dataset_activo, dataset_nombre):
    st.title("🔍 Análisis de Datos")

    df_a_analizar_nombre = st.radio(
        "Selecciona el DataFrame para análisis:",
        ('Original', 'Limpiado'),
        horizontal=True,
        key=f'analisis_selector_{dataset_nombre}'
    )

    df_seleccionado = dataset_activo['df_original'] if df_a_analizar_nombre == 'Original' else dataset_activo['df_limpio']

    st.subheader("📈 Estadísticas Generales")
    metricas = analizar_dataframe(df_seleccionado)
    display_analysis_dashboard(metricas, f"{dataset_nombre} ({df_a_analizar_nombre})")

    st.markdown("---")

    # ✅ NUEVA SECCIÓN: Análisis por variable
    st.subheader("🧪 Análisis por Variable")

    columnas = list(df_seleccionado.columns)
    variable = st.selectbox("Selecciona una variable", columnas, key=f'analisis_variable_selector_{dataset_nombre}')

    descripcion = obtener_descripcion(variable)
    if descripcion:
        st.markdown(f"**Descripción:** {descripcion}")
    else:
        st.markdown(f"**Descripción:** (No encontrada en el diccionario)")

    st.markdown("#### Tabla de Frecuencias")
    tabla = generar_tabla_frecuencias(df_seleccionado, variable)
    st.dataframe(tabla, use_container_width=True)
