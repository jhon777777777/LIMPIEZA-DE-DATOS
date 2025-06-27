# app/components/file_uploader.py
# VERSIÓN FINAL: Un único y simple uploader de archivos.

import streamlit as st
from app.utils.data_loader import cargar_datos

def display_file_uploader():
    """Muestra una interfaz de carga de archivos simple y directa."""
    st.title("⚙️ Analizador Interactivo de Datos (ENAHO)")
    st.write("Sube un archivo de datos (CSV, XLS, XLSX) para comenzar el análisis.")
    
    archivos_subidos = st.file_uploader(
        "Arrastra y suelta tus archivos aquí o haz clic para buscar",
        type=["csv", "xls", "xlsx"], # Se elimina .dta de los tipos aceptados
        accept_multiple_files=True,
        key="main_file_uploader"
    )

    if archivos_subidos:
        for archivo in archivos_subidos:
            # Si el archivo ya está cargado, no hacemos nada
            if archivo.name in st.session_state.datasets:
                continue

            with st.spinner(f"Procesando '{archivo.name}'..."):
                # La función ahora solo devuelve df y msg
                df, msg = cargar_datos(archivo)
                
                if df is not None:
                    # Normalizamos los nombres de columna a minúsculas
                    df.columns = [col.lower() for col in df.columns]
                    
                    # Guardamos solo los DataFrames en el estado
                    st.session_state.datasets[archivo.name] = {
                        'df_original': df,
                        'df_limpio': df.copy()
                    }
                else:
                    st.error(f"Error al cargar '{archivo.name}': {msg}")
        
        # Forzar un re-run para que la UI se actualice con los nuevos datasets
        if 'last_uploaded' not in st.session_state or st.session_state.last_uploaded != [f.name for f in archivos_subidos]:
            st.session_state.last_uploaded = [f.name for f in archivos_subidos]
            st.rerun()
