"""
Métricas de potencial de leads.
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any

from src.core.config import COLORS
from src.core.utils import calculate_lead_score, parse_json_field


def calculate_lead_potential_index(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula el Índice de Potencial de Lead para cada cliente.
    
    Returns:
        Dict con:
        - df_with_scores: DataFrame con scores
        - top_leads: Top 10 leads
        - avg_score: Score promedio
        - chart: Gauge chart
    """
    df_scored = df.copy()
    
    scores = []
    for idx, row in df_scored.iterrows():
        potencial_data = row.get("potencial_upsell", [])
        potencial_upsell = parse_json_field(potencial_data)
        if not potencial_upsell:
            potencial_upsell = []
        
        score = calculate_lead_score(
            volumen_nivel=row.get("volumen_nivel", "Desconocido"),
            urgencia=row.get("urgencia_nivel", "Media"),
            es_pico_estacional=row.get("es_pico_estacional", False),
            potencial_upsell=potencial_upsell,
            volumen_numerico=row.get("volumen_interacciones_semanal", 0) if pd.notna(row.get("volumen_interacciones_semanal")) else None,
            fuente_primaria=row.get("fuente_primaria", ""),
            fuente_detalle=row.get("fuente_detalle", ""),
            sector_principal=row.get("sector_principal", ""),
            transcript=row.get("Transcripcion", "")
        )
        scores.append(score)
    
    df_scored["lead_score"] = scores
    
    base_cols = ["Nombre", "Vendedor asignado", "closed", "lead_score"]
    optional_cols = ["sector_principal", "volumen_nivel", "urgencia_nivel"]
    
    cols_to_show = base_cols + [col for col in optional_cols if col in df_scored.columns]
    
    top_leads = df_scored.nlargest(10, "lead_score")[cols_to_show].copy()
    
    avg_score = df_scored["lead_score"].mean()
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_score,
        title={"text": "Índice de Potencial Promedio"},
        delta={"reference": 50, "increasing": {"color": COLORS["success"]}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": COLORS["primary"]},
            "steps": [
                {"range": [0, 33], "color": COLORS["danger"]},
                {"range": [33, 66], "color": COLORS["warning"]},
                {"range": [66, 100], "color": COLORS["success"]}
            ]
        }
    ))
    
    fig.update_layout(height=400)
    
    return {
        "df_with_scores": df_scored,
        "top_leads": top_leads,
        "avg_score": avg_score,
        "chart": fig
    }
