# app/pages/visualization.py

import streamlit as st
from app.utils.labels_base import (
    listar_variables_por_categoria,
    obtener_descripcion,
    generar_tabla_frecuencias
)

def display(df_limpio, dataset_nombre):
    st.header(f"📊 Exploración de Variables - {dataset_nombre}")
    st.subheader("Descripción de Variables (estilo Stata)")
    st.info("Selecciona una categoría y luego una variable para ver su tabla de frecuencias detallada.")

    # ✅ Llamar categorías desde labels_base
    categorias = listar_variables_por_categoria()

    categoria_seleccionada = st.selectbox(
        "📁 Categoría:",
        list(categorias.keys()),
        key=f"cat_select_{dataset_nombre}"
    )

    variables_en_categoria = [var for var in categorias[categoria_seleccionada] if var in df_limpio.columns]
    
    if not variables_en_categoria:
        st.warning(f"Ninguna variable de la categoría '{categoria_seleccionada}' se encuentra en el dataset actual.")
        st.stop()
    
    variable_seleccionada = st.selectbox(
        "🧪 Variable a describir:",
        variables_en_categoria,
        key=f"var_select_{dataset_nombre}"
    )

    if variable_seleccionada:
        st.markdown("---")
        descripcion = obtener_descripcion(variable_seleccionada)

        col1, col2 = st.columns([1, 3])
        with col1:
            st.write("**Variable:**")
            st.code(variable_seleccionada)
        with col2:
            st.write("**Descripción:**")
            st.success(descripcion or "Sin descripción disponible.")

        tabla_frecuencias = generar_tabla_frecuencias(df_limpio, variable_seleccionada)
        if tabla_frecuencias is not None:
            st.markdown("#### 📋 Tabla de Frecuencias")
            st.dataframe(tabla_frecuencias, use_container_width=True)
        else:
            st.error("No se pudo generar la tabla para esta variable.")
