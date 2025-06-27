# app/visualization/dashboard.py

import streamlit as st
import pandas as pd

def display_analysis_dashboard(metrics, df_name):
    """
    Muestra el dashboard con las métricas de análisis calculadas.
    VERSIÓN MEJORADA: Ahora muestra las tablas de estadísticas descriptivas.
    """
    st.header(f"Dashboard de Análisis: {df_name}")

    # --- Sección de Métricas Generales (sin cambios) ---
    st.subheader("Métricas Generales")
    c1, c2, c3 = st.columns(3)
    c1.metric("Filas", f"{metrics['num_rows']:,}")
    c2.metric("Columnas", f"{metrics['num_cols']:,}")
    c3.metric("Celdas", f"{metrics['total_cells']:,}")
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Duplicados")
        st.metric("Filas Duplicadas", f"{metrics['num_duplicates']:,}", f"{metrics['percent_duplicates']:.2f}%")
    with c2:
        st.subheader("Valores Nulos")
        st.metric("Celdas Vacías", f"{metrics['total_nulls']:,}", f"{metrics['percent_nulls']:.2f}%")

    st.markdown("---")
    
    # --- Sección de Desglose por Columnas (sin cambios) ---
    st.subheader("Desglose por Columnas")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("**Tipos de Datos**")
        st.dataframe(metrics['dtype_counts'], use_container_width=True)
    with c2:
        st.write("**Nulos por Columna**")
        if not metrics['nulls_per_column'].empty:
            st.dataframe(metrics['nulls_per_column'], use_container_width=True)
        else:
            st.info("No hay columnas con valores nulos.")
            
    st.markdown("---")

    # --- NUEVO: Sección de Estadísticas Descriptivas ---
    st.subheader("Estadísticas Descriptivas de las Variables")

    # 1. Para variables numéricas
    st.write("**Variables Numéricas (equivalente a `summarize`)**")
    if not metrics['desc_numericas'].empty:
        # Usamos st.dataframe para una mejor visualización
        st.dataframe(metrics['desc_numericas'])
    else:
        st.info("No se encontraron variables numéricas para analizar.")

    # 2. Para variables categóricas
    st.write("**Variables Categóricas (equivalente a `tabulate`, resumido)**")
    if not metrics['desc_categoricas'].empty:
        st.dataframe(metrics['desc_categoricas'])
    else:
        st.info("No se encontraron variables categóricas para analizar.")