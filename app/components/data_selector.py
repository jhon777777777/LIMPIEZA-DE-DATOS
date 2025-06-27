# app/components/data_selector.py
import streamlit as st

def select_active_dataset():
    st.markdown("---")
    st.header("Selecciona un Dataset para Trabajar")
    nombres_datasets = list(st.session_state.datasets.keys())
    if not nombres_datasets:
        st.warning("No hay datasets cargados.")
        st.stop()
    col1, col2 = st.columns([3, 1])
    with col1:
        dataset_activo_nombre = st.radio("Datasets Cargados:", options=nombres_datasets, horizontal=True, key='dataset_selector')
    with col2:
        if st.button(f"❌ Cerrar '{dataset_activo_nombre}'"):
            del st.session_state.datasets[dataset_activo_nombre]
            st.experimental_rerun()
    if dataset_activo_nombre not in st.session_state.datasets:
        st.stop()
    return dataset_activo_nombre, st.session_state.datasets[dataset_activo_nombre]