# app/main.py
import streamlit as st
from app.components import file_uploader, data_selector
from app.pages import analysis, cleaning, visualization

st.set_page_config(layout="wide", page_title="App de Análisis Multi-Dataset")

if 'datasets' not in st.session_state:
    st.session_state.datasets = {}

file_uploader.display_file_uploader()

if not st.session_state.datasets:
    st.info("Esperando archivos para analizar...")
    st.stop()

dataset_activo_nombre, dataset_activo = data_selector.select_active_dataset()

st.markdown("---")
modo = st.radio(
    "Elige un modo de operación:",
    ('🔍 Análisis General', '🧹 Limpieza y Transformación', '📊 Visualización de Datos'),
    horizontal=True, key=f'modo_{dataset_activo_nombre}'
)

if modo == '🔍 Análisis General':
    analysis.display(dataset_activo, dataset_activo_nombre)
elif modo == '🧹 Limpieza y Transformación':
    cleaning.display(dataset_activo, dataset_activo_nombre)
elif modo == '📊 Visualización de Datos':
    visualization.display(dataset_activo['df_limpio'], dataset_activo_nombre)
    
    
    
    