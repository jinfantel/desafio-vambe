"""
API pública para métricas de tasa de cierre.
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any

from src.core.config import COLORS
from .calculations import calculate_monthly_stats, prepare_heatmap_data, create_hover_text
from .charts import create_close_rate_chart, create_empty_heatmap


def calculate_global_close_rate(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula la tasa de cierre global y genera pronóstico para los próximos 6 meses.
    
    Returns:
        Dict con:
        - current_rate: Tasa actual
        - predicted_6m: Tasa proyectada promedio para los próximos 6 meses
        - monthly_data: DataFrame con datos mensuales
        - chart: Figura de Plotly
    """
    current_rate = df["closed"].mean()
    
    monthly_stats = calculate_monthly_stats(df)
    
    chart, predicted_6m = create_close_rate_chart(monthly_stats)
    
    return {
        "current_rate": current_rate,
        "predicted_6m": predicted_6m,
        "monthly_data": monthly_stats,
        "chart": chart
    }


def calculate_close_rate_by_seller(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula la tasa de cierre por vendedor con gráfico de barras horizontales.
    
    Returns:
        Dict con:
        - seller_stats: DataFrame con estadísticas por vendedor
        - chart: Figura de Plotly
    """
    seller_stats = df.groupby("Vendedor asignado").agg({
        "closed": ["sum", "count", "mean"]
    }).reset_index()
    
    seller_stats.columns = ["vendedor", "closed_count", "total", "close_rate"]
    seller_stats = seller_stats.sort_values("close_rate", ascending=True)
    
    avg_rate = df["closed"].mean()
    
    fig = go.Figure()
    
    colors_list = [
        COLORS["success"] if rate >= avg_rate else COLORS["danger"]
        for rate in seller_stats["close_rate"]
    ]
    
    fig.add_trace(go.Bar(
        y=seller_stats["vendedor"],
        x=seller_stats["close_rate"],
        orientation="h",
        marker=dict(color=colors_list),
        text=[f"{rate:.1%}" for rate in seller_stats["close_rate"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Tasa: %{x:.1%}<br>Cerrados: %{customdata[0]}/%{customdata[1]}<extra></extra>",
        customdata=seller_stats[["closed_count", "total"]].values
    ))
    
    fig.add_vline(
        x=avg_rate,
        line_dash="dash",
        line_color=COLORS["primary"],
        line_width=2,
        annotation_text=f"Promedio: {avg_rate:.1%}",
        annotation_position="top",
        annotation=dict(
            yshift=10,
            font=dict(size=12, color=COLORS["primary"]),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor=COLORS["primary"],
            borderwidth=1,
            borderpad=4
        )
    )
    
    fig.update_layout(
        title="Tasa de Cierre por Vendedor (orden ascendente)",
        xaxis_title="Tasa de Cierre",
        yaxis_title="",
        xaxis_tickformat=".0%",
        height=400,
        showlegend=False
    )
    
    return {
        "seller_stats": seller_stats,
        "chart": fig
    }


def calculate_close_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Genera un heatmap de tasa de cierre: Sector Principal × Volumen Nivel.
    
    Returns:
        Figura de Plotly con heatmap
    """
    if "sector_principal" not in df.columns or "volumen_nivel" not in df.columns:
        return create_empty_heatmap("⚠️ Ejecuta la categorización primero para ver esta métrica")
    
    df_cat = df[df["sector_principal"].notna() & df["volumen_nivel"].notna()].copy()
    
    if len(df_cat) == 0:
        return create_empty_heatmap(
            "No hay datos categorizados aún. Ejecuta la categorización primero.",
            color="text",
            size=14
        )
    
    close_rate_pivot, count_pivot, _ = prepare_heatmap_data(df_cat)
    
    hover_text = create_hover_text(close_rate_pivot, count_pivot)
    
    fig = go.Figure(data=go.Heatmap(
        z=close_rate_pivot.values,
        x=close_rate_pivot.columns,
        y=close_rate_pivot.index,
        colorscale=[
            [0, COLORS["danger"]],
            [0.5, COLORS["warning"]],
            [1, COLORS["success"]]
        ],
        text=[[f"{val:.0%}" for val in row] for row in close_rate_pivot.values],
        texttemplate="%{text}",
        textfont={"size": 12, "color": "white"},
        hovertext=hover_text,
        hoverinfo="text",
        colorbar=dict(
            title="Tasa Cierre",
            tickformat=".0%"
        )
    ))
    
    fig.update_layout(
        title="Sweet Spots: Sector × Volumen (Tasa de Cierre)",
        xaxis_title="Nivel de Volumen",
        yaxis_title="Sector Principal",
        height=500
    )
    
    return fig
