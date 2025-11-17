"""
Métricas de preocupaciones que afectan el cierre.
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any

from src.core.config import COLORS
from src.core.utils import parse_json_field


def calculate_top_concerns(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Identifica las preocupaciones que más afectan el cierre.
    
    Returns:
        Dict con:
        - concern_stats: DataFrame con estadísticas
        - chart: Figura de Plotly
    """
    concerns_list = []
    
    for idx, row in df.iterrows():
        preocupaciones_data = row.get("preocupaciones")
        preocupaciones = parse_json_field(preocupaciones_data)
        
        if preocupaciones and isinstance(preocupaciones, list):
            for concern in preocupaciones:
                if isinstance(concern, dict):
                    concerns_list.append({
                        "tipo": concern.get("tipo", "Otra"),
                        "closed": row["closed"],
                        "nombre": row["Nombre"]
                    })
    
    if len(concerns_list) == 0:
        return {"concern_stats": pd.DataFrame(), "chart": go.Figure()}
    
    concerns_df = pd.DataFrame(concerns_list)
    
    concern_stats = concerns_df.groupby("tipo").agg({
        "closed": ["count", lambda x: (x == 0).sum(), "mean"]
    }).reset_index()
    
    concern_stats.columns = ["tipo", "total", "no_closed_count", "close_rate"]
    concern_stats["no_close_percentage"] = concern_stats["no_closed_count"] / concern_stats["total"]
    concern_stats = concern_stats.sort_values("no_close_percentage", ascending=False).head(5)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=concern_stats["tipo"],
        y=concern_stats["no_close_percentage"],
        marker_color=COLORS["danger"],
        text=[f"{val:.1%}" for val in concern_stats["no_close_percentage"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>% No-Cierre: %{y:.1%}<br>Total leads: %{customdata}<extra></extra>",
        customdata=concern_stats["total"]
    ))
    
    fig.update_layout(
        title="Top 5 Preocupaciones que más Afectan el Cierre",
        xaxis_title="Tipo de Preocupación",
        yaxis_title="% de No-Cierres",
        yaxis_tickformat=".0%",
        height=450
    )
    
    return {
        "concern_stats": concern_stats,
        "chart": fig,
        "concerns_df": concerns_df
    }
