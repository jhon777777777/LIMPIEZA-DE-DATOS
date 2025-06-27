# app/pages/cleaning.py
# VERSIÓN FINAL: Usa una lista vertical de checkboxes para la selección de variables.

import streamlit as st
import pandas as pd
from app.utils.data_cleaner import limpiar_dataframe
from app.utils.labels_base import VARIABLE_DESCRIPTIONS

def display(dataset_activo, dataset_nombre):
    """
    Muestra la página de Limpieza y Transformación con una lista vertical
    de checkboxes para una selección de columnas clara y organizada.
    """
    
    with st.sidebar:
        st.header(f"Opciones para: {dataset_nombre}")

        # --- Sección de Limpieza (Nulos y Duplicados) ---
        st.subheader("Opciones de Limpieza")
        op_nulos_num = st.selectbox("Nulos numéricos:", ["No hacer nada", "Eliminar filas con nulos", "Rellenar con la media", "Rellenar con la mediana"], key=f'nulos_num_{dataset_nombre}')
        op_nulos_cat = st.selectbox("Nulos categóricos:", ["No hacer nada", "Rellenar con la moda", "Rellenar con 'Desconocido'"], key=f'nulos_cat_{dataset_nombre}')
        eliminar_dup = st.checkbox("Eliminar duplicados", key=f'duplicados_{dataset_nombre}')
        
        st.markdown("---")

        # --- NUEVO: Lista Vertical de Checkboxes para Seleccionar Variables ---
        st.subheader("Columnas a Mantener")

        columnas_originales = dataset_activo['df_original'].columns.tolist()
        
        # 1. Definimos una clave única para guardar el estado de los checkboxes
        checkbox_state_key = f'column_states_{dataset_nombre}'
        
        # 2. Inicializamos el estado si no existe
        if checkbox_state_key not in st.session_state:
            st.session_state[checkbox_state_key] = {
                col: col in dataset_activo['df_limpio'].columns for col in columnas_originales
            }

        # 3. Creamos un contenedor para que la lista tenga scroll si es muy larga
        with st.container(height=300): # Puedes ajustar la altura (height) como desees
            # 4. Iteramos y creamos un checkbox por cada variable, uno debajo del otro
            for col_name in columnas_originales:
                label = f"{col_name} - {VARIABLE_DESCRIPTIONS.get(col_name.lower(), '')}"
                
                st.session_state[checkbox_state_key][col_name] = st.checkbox(
                    label, 
                    value=st.session_state[checkbox_state_key][col_name], 
                    key=f"check_{col_name}_{dataset_nombre}"
                )

        st.markdown("---")

        # 5. El botón "Aplicar" funciona igual que antes, leyendo el estado guardado
        if st.button("Aplicar Cambios Manuales", key=f'aplicar_{dataset_nombre}', type="primary"):
            cols_reales_a_mantener = [
                col for col, is_checked in st.session_state[checkbox_state_key].items() if is_checked
            ]
            
            df_procesado = limpiar_dataframe(
                dataset_activo['df_original'], 
                op_nulos_num, 
                op_nulos_cat, 
                eliminar_dup, 
                cols_reales_a_mantener
            )
            dataset_activo['df_limpio'] = df_procesado
            
            st.session_state[checkbox_state_key] = {
                col: col in df_procesado.columns for col in columnas_originales
            }
            
            st.success("¡Cambios de limpieza aplicados!")
            st.experimental_rerun()
            
    # --- La vista principal no necesita cambios ---
    st.header(f"Vista Previa y Descarga: {dataset_nombre}")
    tab_original, tab_limpio = st.tabs(["📄 Datos Originales", "✨ Datos Limpiados"])
    with tab_original:
        st.dataframe(dataset_activo['df_original'])
    with tab_limpio:
        st.dataframe(dataset_activo['df_limpio'])
        st.markdown("---")
        csv = dataset_activo['df_limpio'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar CSV Limpio",
            data=csv,
            file_name=f"limpio_{dataset_nombre}.csv",
            mime='text/csv'
        )