# app/utils/data_cleaner.py

import pandas as pd

def limpiar_dataframe(df, opcion_nulos_num, opcion_nulos_cat, eliminar_duplicados, columnas_a_mantener):
    """
    Aplica las operaciones de limpieza seleccionadas al DataFrame.
    Esta función solo procesa datos, no muestra nada en la UI.
    """
    df_limpio = df.copy()

    # 1. Selección de columnas
    # Asegura que solo se usan columnas que existen en el dataframe
    columnas_validas = [col for col in columnas_a_mantener if col in df_limpio.columns]
    df_limpio = df_limpio[columnas_validas]

    # 2. Manejo de nulos
    if opcion_nulos_num == "Eliminar filas con nulos":
        # Nota: Esto eliminará filas con CUALQUIER nulo, no solo numérico. Es un comportamiento común.
        df_limpio.dropna(inplace=True)
    else:
        # Lógica para nulos numéricos
        numeric_cols = df_limpio.select_dtypes(include='number').columns
        if opcion_nulos_num == "Rellenar con la media":
            df_limpio[numeric_cols] = df_limpio[numeric_cols].fillna(df_limpio[numeric_cols].mean())
        elif opcion_nulos_num == "Rellenar con la mediana":
            df_limpio[numeric_cols] = df_limpio[numeric_cols].fillna(df_limpio[numeric_cols].median())

        # Lógica para nulos categóricos
        cat_cols = df_limpio.select_dtypes(include=['object', 'category']).columns
        if opcion_nulos_cat == "Rellenar con la moda":
            # Rellenar cada columna con su propia moda
            for col in cat_cols:
                if not df_limpio[col].mode().empty:
                    df_limpio[col].fillna(df_limpio[col].mode()[0], inplace=True)
        elif opcion_nulos_cat == "Rellenar con 'Desconocido'":
            df_limpio[cat_cols] = df_limpio[cat_cols].fillna('Desconocido')

    # 3. Eliminar duplicados
    if eliminar_duplicados:
        df_limpio.drop_duplicates(inplace=True)

    # 4. Resetear el índice para evitar problemas futuros
    df_limpio.reset_index(drop=True, inplace=True)
    
    return df_limpio