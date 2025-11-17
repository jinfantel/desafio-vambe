"""
Métricas de oportunidades de upsell.
"""

import pandas as pd
import plotly.graph_objects as go

from src.core.config import COLORS
from src.core.utils import parse_json_field


def calculate_upsell_radar(df: pd.DataFrame) -> go.Figure:
    """
    Radar chart con el % de clientes que mencionan cada add-on.
    
    Returns:
        Figura de Plotly (radar chart)
    """
    upsell_list = []
    
    for idx, row in df.iterrows():
        upsell_data = row.get("potencial_upsell")
        upsell = parse_json_field(upsell_data)
        
        if upsell and isinstance(upsell, list):
            for item in upsell:
                upsell_list.append(item)
    
    if len(upsell_list) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="⚠️ Ejecuta la categorización primero para ver esta métrica",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS["warning"])
        )
        return fig
    
    upsell_counts = pd.Series(upsell_list).value_counts()
    
    if upsell_counts.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos de oportunidades de upsell disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    total_leads = len(df)
    upsell_percentages = (upsell_counts / total_leads * 100).round(1)
    
    fig = go.Figure()
    
    r_values = list(upsell_percentages.values) + [upsell_percentages.values[0]]
    theta_values = list(upsell_percentages.index) + [upsell_percentages.index[0]]
    
    fig.add_trace(go.Scatterpolar(
        r=r_values,
        theta=theta_values,
        fill="toself",
        fillcolor=COLORS["info"],
        opacity=0.6,
        line=dict(color=COLORS["primary"], width=2),
        marker=dict(size=8, color=COLORS["primary"]),
        hovertemplate="<b>%{theta}</b><br>%{r:.1f}% de leads<extra></extra>"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(upsell_percentages.values) * 1.2],
                showticklabels=True,
                ticks="outside",
                tickfont=dict(size=11, color="black")
            ),
            angularaxis=dict(
                showticklabels=True,
                tickfont=dict(size=12, color="black"),
                rotation=90
            )
        ),
        title="Oportunidades de Upsell (% de Leads que lo necesitan)",
        height=550,
        showlegend=False,
        margin=dict(t=80, b=80, l=100, r=100)
    )
    
    return fig
