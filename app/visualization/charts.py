# app/visualization/charts.py

import plotly.express as px
import pandas as pd

def plot_histogram(df, column, color_col=None):
    """Genera un histograma interactivo."""
    title = f'<b>Distribución de: {column}</b>'
    if color_col:
        title += f' (coloreado por {color_col})'
    fig = px.histogram(df, x=column, title=title, template='plotly_white', color=color_col,
                       color_discrete_sequence=px.colors.qualitative.Plotly if color_col else ['#0083B8'])
    fig.update_layout(title_x=0.5, bargap=0.1)
    return fig

def plot_bar_chart(df, column):
    """Genera un gráfico de barras interactivo de frecuencias."""
    if column not in df.columns:
        return None
    value_counts = df[column].value_counts().reset_index()
    value_counts.columns = [column, 'Frecuencia']
    title = f'<b>Frecuencia de categorías en: {column}</b>'
    fig = px.bar(value_counts, x=column, y='Frecuencia', title=title, text_auto=True, template='plotly_white', color_discrete_sequence=['#0083B8'])
    fig.update_traces(textposition='outside')
    fig.update_layout(title_x=0.5)
    return fig

def plot_scatter(df, x_column, y_column, color_col=None):
    """Genera un gráfico de dispersión interactivo con línea de tendencia."""
    if x_column not in df.columns or y_column not in df.columns:
        return None
    title = f'<b>Relación entre {x_column} y {y_column}</b>'
    if color_col:
        title += f' (coloreado por {color_col})'
    fig = px.scatter(df, x=x_column, y=y_column, title=title, template='plotly_white', trendline="ols", color=color_col,
                     color_discrete_sequence=px.colors.qualitative.Plotly if color_col else ['#0083B8'])
    fig.update_layout(title_x=0.5)
    return fig
    
def plot_box_plot(df, num_column, cat_column=None):
    """Genera un diagrama de caja interactivo."""
    if num_column not in df.columns:
        return None
    title = f'<b>Diagrama de Caja de {num_column}</b>'
    if cat_column and cat_column in df.columns:
        title += f' (agrupado por {cat_column})'
    fig = px.box(df, y=num_column, x=cat_column, title=title, template='plotly_white', color=cat_column, color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_layout(title_x=0.5)
    return fig

def plot_correlation_heatmap(df):
    """Genera un mapa de calor de correlaciones para columnas numéricas."""
    numeric_df = df.select_dtypes(include='number')
    if numeric_df.shape[1] < 2:
        return None
    corr_matrix = numeric_df.corr()
    title = '<b>Mapa de Calor de Correlaciones Numéricas</b>'
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", title=title, template='plotly_white', color_continuous_scale='RdBu_r')
    fig.update_layout(title_x=0.5)
    return fig