"""
Tab Deep Analysis - Análisis profundo de datos.
"""

import streamlit as st
import pandas as pd

from src.analytics import calculate_close_heatmap, calculate_source_roi
from ..components import render_chart_with_expander


def render_deep_analysis_tab(df: pd.DataFrame) -> None:
    """
    Renderiza la pestaña de Análisis Profundo.
    
    Args:
        df: DataFrame filtrado con los datos
    """
    st.header("🔬 Análisis Profundo")
    
    st.subheader("Sweet Spots: Sector × Volumen")
    heatmap = calculate_close_heatmap(df)
    st.plotly_chart(heatmap, use_container_width=True, key="deep_heatmap")
    
    st.markdown("---")
    
    _render_source_roi(df)


def _render_source_roi(df: pd.DataFrame) -> None:
    """Renderiza el análisis de ROI de fuentes de descubrimiento."""
    st.subheader("ROI de Fuentes de Descubrimiento")
    
    source_roi_data = calculate_source_roi(df)
    
    st.plotly_chart(source_roi_data["chart"], use_container_width=True, key="deep_source_roi")
    
    if len(source_roi_data["source_stats"]) > 0:
        st.markdown("**📊 Tabla Completa con Score ROI**")
        st.dataframe(
            source_roi_data["source_stats"].style.format({
                "close_rate": "{:.1%}",
                "lead_percentage": "{:.1%}",
                "roi_score": "{:.3f}",
                "closed_count": "{:.0f}",
                "total": "{:.0f}"
            }).background_gradient(subset=["roi_score"], cmap="Greens"),
            use_container_width=True
        )
