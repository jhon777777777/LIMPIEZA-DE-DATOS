# app/utils/data_loader.py
# VERSIÓN FINAL Y SIMPLE: Carga datos de formatos estándar (CSV, Excel).

import pandas as pd
import streamlit as st

# ESTA ES LA FUNCIÓN 'cargar_datos' QUE TU APP ESTÁ BUSCANDO
@st.cache_data
def cargar_datos(archivo_subido):
    """
    Carga datos desde un archivo CSV o Excel subido por el usuario.
    Maneja diferentes codificaciones de texto para CSV.
    """
    try:
        extension = archivo_subido.name.split('.')[-1].lower()
        
        if extension == 'csv':
            # Intenta con varias codificaciones comunes para máxima compatibilidad
            encodings_to_try = ['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1']
            df = None
            for encoding in encodings_to_try:
                try:
                    archivo_subido.seek(0)
                    df = pd.read_csv(archivo_subido, sep=None, engine='python', encoding=encoding)
                    break # Si la lectura es exitosa, se detiene el bucle
                except (UnicodeDecodeError, AttributeError):
                    continue
            
            if df is None:
                return None, "No se pudo decodificar el archivo CSV con las codificaciones comunes."

        elif extension in ['xls', 'xlsx']:
            df = pd.read_excel(archivo_subido)
            
        else:
            return None, f"Formato de archivo '{extension}' no soportado. Por favor, sube un CSV o Excel."
            
        return df, "¡Archivo cargado exitosamente!"

    except Exception as e:
        return None, f"Error al procesar el archivo: {e}"