"""
Componentes de display de métricas.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List


def render_metric_card(label: str, value: str, delta: str = None, help_text: str = None) -> None:
    """
    Renderiza una tarjeta de métrica individual.
    
    Args:
        label: Etiqueta de la métrica
        value: Valor principal a mostrar
        delta: Cambio o comparación (opcional)
        help_text: Texto de ayuda (opcional)
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text
    )


def render_metrics_grid(metrics: List[Dict[str, Any]], columns: int = 3) -> None:
    """
    Renderiza una grilla de métricas.
    
    Args:
        metrics: Lista de dicts con keys: label, value, delta, help_text
        columns: Número de columnas en la grilla
    """
    cols = st.columns(columns)
    
    for idx, metric in enumerate(metrics):
        with cols[idx % columns]:
            render_metric_card(
                label=metric.get('label', ''),
                value=metric.get('value', ''),
                delta=metric.get('delta'),
                help_text=metric.get('help_text')
            )


def render_chart_with_expander(
    chart_fig,
    expander_title: str = None,
    expander_df: pd.DataFrame = None,
    df_format: Dict[str, str] = None,
    use_container_width: bool = True
) -> None:
    """
    Renderiza un gráfico con expander opcional para ver tabla detallada.
    
    Args:
        chart_fig: Figura de Plotly
        expander_title: Título del expander (si None, no muestra expander)
        expander_df: DataFrame a mostrar en el expander
        df_format: Dict con formato de columnas para el DataFrame
        use_container_width: Si usar ancho completo del contenedor
    """
    st.plotly_chart(chart_fig, use_container_width=use_container_width)
    
    if expander_title and expander_df is not None:
        with st.expander(expander_title):
            if df_format:
                st.dataframe(
                    expander_df.style.format(df_format),
                    use_container_width=True
                )
            else:
                st.dataframe(expander_df, use_container_width=True)
