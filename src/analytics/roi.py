"""
Métricas de ROI de fuentes de descubrimiento.
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any

from src.core.config import COLORS


def calculate_source_roi(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula el ROI de cada fuente de descubrimiento.
    ROI Score = (% leads × % cierre)
    
    Returns:
        Dict con:
        - source_stats: DataFrame con estadísticas
        - chart: Figura de Plotly
    """
    if "fuente_primaria" not in df.columns:
        return {
            "source_stats": pd.DataFrame(),
            "chart": go.Figure().add_annotation(
                text="⚠️ Ejecuta la categorización primero para ver esta métrica",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color=COLORS["warning"])
            )
        }
    
    df_cat = df[df["fuente_primaria"].notna()].copy()
    
    if len(df_cat) == 0:
        return {"source_stats": pd.DataFrame(), "chart": go.Figure()}
    
    source_stats = df_cat.groupby("fuente_primaria").agg({
        "closed": ["sum", "count", "mean"]
    }).reset_index()
    
    source_stats.columns = ["fuente", "closed_count", "total", "close_rate"]
    
    total_leads = len(df_cat)
    source_stats["lead_percentage"] = source_stats["total"] / total_leads
    
    source_stats["roi_score"] = source_stats["lead_percentage"] * source_stats["close_rate"]
    
    source_stats = source_stats.sort_values("roi_score", ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name="% Leads",
        x=source_stats["fuente"],
        y=source_stats["lead_percentage"],
        marker_color=COLORS["info"],
        text=[f"{val:.1%}" for val in source_stats["lead_percentage"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>% Leads: %{y:.1%}<extra></extra>"
    ))
    
    fig.add_trace(go.Bar(
        name="% Cierre",
        x=source_stats["fuente"],
        y=source_stats["close_rate"],
        marker_color=COLORS["success"],
        text=[f"{val:.1%}" for val in source_stats["close_rate"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>% Cierre: %{y:.1%}<extra></extra>"
    ))
    
    fig.update_layout(
        title="ROI de Fuentes de Descubrimiento",
        xaxis_title="Fuente",
        yaxis_title="Porcentaje",
        yaxis_tickformat=".0%",
        barmode="group",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return {
        "source_stats": source_stats,
        "chart": fig
    }
