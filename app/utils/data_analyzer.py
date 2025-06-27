# app/utils/data_analyzer.py

import pandas as pd
from app.utils.labels_base import obtener_descripcion  # ✅ Agregamos labels

def analizar_dataframe(df):
    """
    Realiza un análisis completo de un DataFrame y devuelve las métricas.
    Versión enriquecida con descripciones desde labels_base.
    """

    # Métricas generales
    num_rows, num_cols = df.shape
    total_cells = num_rows * num_cols
    num_duplicates = df.duplicated().sum()
    percent_duplicates = (num_duplicates / num_rows) * 100 if num_rows > 0 else 0
    total_nulls = df.isnull().sum().sum()
    percent_nulls = (total_nulls / total_cells) * 100 if total_cells > 0 else 0

    # Tipos de datos
    dtype_counts = df.dtypes.astype(str).value_counts().reset_index()
    dtype_counts.columns = ['Tipo de Dato', 'Cantidad']

    # Columnas con valores nulos
    nulls_per_column = df.isnull().sum().reset_index()
    nulls_per_column.columns = ['Columna', 'Nulos']
    nulls_per_column = nulls_per_column[nulls_per_column['Nulos'] > 0].sort_values(by='Nulos', ascending=False)

    # Estadísticas descriptivas
    desc_numericas = df.describe(include='number').T.reset_index()
    desc_numericas.rename(columns={'index': 'Variable'}, inplace=True)
    desc_numericas['Descripción'] = desc_numericas['Variable'].apply(lambda var: obtener_descripcion(var) or "Sin descripción")

    desc_categoricas = df.describe(include=['object', 'category']).T.reset_index()
    desc_categoricas.rename(columns={'index': 'Variable'}, inplace=True)
    desc_categoricas['Descripción'] = desc_categoricas['Variable'].apply(lambda var: obtener_descripcion(var) or "Sin descripción")

    # Empaquetar resultados
    return {
        "num_rows": num_rows,
        "num_cols": num_cols,
        "total_cells": total_cells,
        "num_duplicates": num_duplicates,
        "percent_duplicates": percent_duplicates,
        "total_nulls": total_nulls,
        "percent_nulls": percent_nulls,
        "dtype_counts": dtype_counts,
        "nulls_per_column": nulls_per_column,
        "desc_numericas": desc_numericas,
        "desc_categoricas": desc_categoricas,
    }
