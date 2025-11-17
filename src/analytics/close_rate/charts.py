"""
Funciones para creación de gráficos de tasas de cierre.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import List, Tuple

from src.core.config import COLORS
from .calculations import calculate_forecast


def add_actual_trace(fig: go.Figure, monthly_stats: pd.DataFrame) -> None:
    """
    Añade traza de datos reales al gráfico.
    
    Args:
        fig: Figura de Plotly
        monthly_stats: DataFrame con estadísticas mensuales
    """
    fig.add_trace(go.Scatter(
        x=monthly_stats["month_name"],
        y=monthly_stats["close_rate"],
        mode="lines+markers",
        name="Tasa de Cierre",
        line=dict(color=COLORS["primary"], width=3),
        marker=dict(size=10, color=COLORS["primary"]),
        hovertemplate="<b>%{x}</b><br>Tasa: %{y:.1%}<extra></extra>"
    ))


def add_trend_trace(fig: go.Figure, monthly_stats: pd.DataFrame) -> None:
    """
    Añade línea de tendencia al gráfico.
    
    Args:
        fig: Figura de Plotly
        monthly_stats: DataFrame con estadísticas mensuales
    """
    x_numeric = np.arange(len(monthly_stats))
    y = monthly_stats["close_rate"].values
    
    coeffs = np.polyfit(x_numeric, y, 1)
    trend_line = coeffs[0] * x_numeric + coeffs[1]
    
    fig.add_trace(go.Scatter(
        x=monthly_stats["month_name"],
        y=trend_line,
        mode="lines",
        name="Tendencia",
        line=dict(color=COLORS["success"], width=2, dash="dash"),
        hovertemplate="Tendencia: %{y:.1%}<extra></extra>"
    ))


def add_forecast_trace(fig: go.Figure, future_y: np.ndarray, future_months: List[str]) -> None:
    """
    Añade traza de proyección al gráfico.
    
    Args:
        fig: Figura de Plotly
        future_y: Valores proyectados
        future_months: Nombres de meses futuros
    """
    fig.add_trace(go.Scatter(
        x=future_months,
        y=future_y,
        mode="lines+markers",
        name="Proyección 6 meses",
        line=dict(color=COLORS["warning"], width=2, dash="dot"),
        marker=dict(size=8, color=COLORS["warning"], symbol="diamond"),
        hovertemplate="<b>%{x}</b><br>Proyección: %{y:.1%}<extra></extra>"
    ))


def create_close_rate_chart(monthly_stats: pd.DataFrame) -> Tuple[go.Figure, float]:
    """
    Crea gráfico completo de tasa de cierre con proyección.
    
    Args:
        monthly_stats: DataFrame con estadísticas mensuales
        
    Returns:
        Tuple con (figura de Plotly, tasa proyectada promedio)
    """
    fig = go.Figure()
    predicted_6m = monthly_stats["close_rate"].mean()
    
    add_actual_trace(fig, monthly_stats)
    
    if len(monthly_stats) >= 2:
        add_trend_trace(fig, monthly_stats)
        
        future_y, future_months, predicted_6m = calculate_forecast(monthly_stats)
        add_forecast_trace(fig, future_y, future_months)
    
    fig.update_layout(
        title="Evolución Mensual y Proyección (próximos 6 meses)",
        xaxis_title="Mes",
        yaxis_title="Tasa de Cierre",
        yaxis_tickformat=".0%",
        hovermode="x unified",
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig, predicted_6m


def create_empty_heatmap(message: str, color: str = "warning", size: int = 16) -> go.Figure:
    """
    Crea heatmap vacío con mensaje.
    
    Args:
        message: Mensaje a mostrar
        color: Color del texto
        size: Tamaño de fuente
        
    Returns:
        Figura de Plotly vacía con mensaje
    """
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=size, color=COLORS.get(color, COLORS["warning"]))
    )
    fig.update_layout(height=400)
    return fig
