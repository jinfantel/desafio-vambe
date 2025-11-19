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
    categorias_fijas = [
        "Integración con CRM/Tickets existente",
        "Soporte multicanal (WhatsApp, IG, Email, etc.)",
        "Escalamiento automático en temporada alta / picos",
        "Respuestas personalizadas con tono de marca",
        "Reportes y analíticos de atención al cliente"
    ]
    
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
    
    total_leads = len(df)
    
    upsell_percentages = {}
    for categoria in categorias_fijas:
        count = upsell_counts.get(categoria, 0)
        upsell_percentages[categoria] = round((count / total_leads) * 100, 1)
    
    fig = go.Figure()
    
    r_values = list(upsell_percentages.values()) + [list(upsell_percentages.values())[0]]
    theta_values = list(upsell_percentages.keys()) + [list(upsell_percentages.keys())[0]]
    
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
                range=[0, 50],
                showticklabels=True,
                ticks="outside",
                tickfont=dict(size=11, color="black"),
                tickvals=[0, 10, 20, 30, 40, 50],
                ticktext=["0%", "10%", "20%", "30%", "40%", "50%"]
            ),
            angularaxis=dict(
                showticklabels=True,
                tickfont=dict(size=11, color="black"),
                rotation=90
            )
        ),
        title="Oportunidades de Upsell (% de Leads que lo necesitan)",
        height=600,
        showlegend=False,
        margin=dict(t=100, b=100, l=120, r=120)
    )
    
    return fig
