"""
Métricas de distribución de volumen.
"""

import pandas as pd
import plotly.graph_objects as go

from src.core.config import COLORS


def calculate_volume_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Boxplot/Violin plot de volumen numérico según cierre.
    
    Returns:
        Figura de Plotly
    """
    if "volumen_numerico" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="⚠️ Ejecuta la categorización primero para ver esta métrica",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS["warning"])
        )
        return fig
    
    df_vol = df[df["volumen_numerico"].notna()].copy()
    
    if len(df_vol) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos de volumen numérico disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    df_vol["status"] = df_vol["closed"].apply(lambda x: "Cerrados" if x == 1 else "No Cerrados")
    
    fig = go.Figure()
    
    for status, color in [("Cerrados", COLORS["success"]), ("No Cerrados", COLORS["danger"])]:
        data = df_vol[df_vol["status"] == status]["volumen_numerico"]
        
        fig.add_trace(go.Violin(
            y=data,
            name=status,
            box_visible=True,
            meanline_visible=True,
            fillcolor=color,
            opacity=0.6,
            x0=status,
            hovertemplate="<b>%{x}</b><br>Volumen: %{y}<extra></extra>"
        ))
    
    fig.update_layout(
        title="Distribución de Volumen Numérico: Cerrados vs No Cerrados",
        yaxis_title="Volumen de Interacciones",
        xaxis_title="",
        height=450,
        showlegend=False
    )
    
    return fig
