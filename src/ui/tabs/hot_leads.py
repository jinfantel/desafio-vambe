"""
Tab Hot Leads - Priorización de leads.
"""

import streamlit as st
import pandas as pd

from src.analytics import calculate_lead_potential_index
from ..components import render_lead_table, render_transcript_viewer


def render_hot_leads_tab(df: pd.DataFrame) -> None:
    """
    Renderiza la pestaña de Hot Leads.
    
    Args:
        df: DataFrame filtrado con los datos
    """
    st.header("🔥 Hot Leads - Priorización de Follow-up")
    
    lead_potential_data = calculate_lead_potential_index(df)
    df_with_scores = lead_potential_data["df_with_scores"]
    
    df_hot_leads = df_with_scores.sort_values("lead_score", ascending=False)
    
    st.markdown("**Tabla Completa con Índice de Potencial**")
    
    display_cols = [
        "Nombre", "Vendedor asignado", "Fecha de la Reunion",
        "closed", "lead_score", "sector_principal", "volumen_nivel",
        "urgencia_nivel", "fuente_primaria"
    ]
    
    render_lead_table(
        df=df_hot_leads,
        display_columns=display_cols,
        format_dict={
            "lead_score": "{:.1f}",
            "closed": lambda x: "✅" if x == 1 else "❌",
            "Fecha de la Reunion": lambda x: x.strftime("%Y-%m-%d")
        },
        height=600,
        gradient_column="lead_score"
    )
    
    st.markdown("---")
    
    render_transcript_viewer(df_hot_leads)
