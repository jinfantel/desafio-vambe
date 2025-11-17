"""
Tab Concerns - Análisis de preocupaciones.
"""

import streamlit as st
import pandas as pd

from src.analytics import calculate_top_concerns
from ..components import render_concerns_table, render_concerns_explorer


def render_concerns_tab(df: pd.DataFrame) -> None:
    """
    Renderiza la pestaña de Preocupaciones.
    
    Args:
        df: DataFrame filtrado con los datos
    """
    st.header("⚠️ Análisis de Preocupaciones - Barreras de Cierre")
    
    concerns_data = calculate_top_concerns(df)
    
    if len(concerns_data.get("concern_stats", [])) > 0:
        st.plotly_chart(
            concerns_data["chart"],
            use_container_width=True,
            key="concerns_tab_main_chart"
        )
        
        st.markdown("---")
        
        concern_summary = render_concerns_table(concerns_data["concerns_df"])
        
        st.markdown("---")
        
        render_concerns_explorer(df, concerns_data["concerns_df"])
    else:
        st.info("No hay datos de preocupaciones disponibles. Ejecuta la categorización primero.")
