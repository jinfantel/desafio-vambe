"""
Tab Overview - Métricas principales de ventas.
"""

import streamlit as st
import pandas as pd

from src.analytics import (
    calculate_global_close_rate,
    calculate_close_rate_by_seller,
    calculate_volume_distribution,
    calculate_lead_potential_index,
    calculate_upsell_radar
)
from ..components import render_chart_with_expander


def render_overview_tab(df: pd.DataFrame) -> None:
    """
    Renderiza la pestaña de Overview con las métricas principales.
    
    Args:
        df: DataFrame filtrado con los datos
    """
    st.header("📊 Métricas Clave de Ventas")
    
    _render_global_close_rate(df)
    st.markdown("---")
    
    _render_seller_close_rate(df)
    st.markdown("---")
    
    _render_lead_potential_index(df)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        _render_volume_distribution(df)
    
    with col2:
        _render_upsell_opportunities(df)


def _render_global_close_rate(df: pd.DataFrame) -> None:
    """Renderiza la métrica de tasa de cierre global con pronóstico."""
    st.subheader("Tasa de Cierre Global + Pronóstico 6 meses")
    
    close_rate_data = calculate_global_close_rate(df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Tasa Actual",
            f"{close_rate_data['current_rate']:.1%}",
            delta=f"{(close_rate_data['current_rate'] - 0.5) * 100:.1f}% vs 50%"
        )
    with col2:
        st.metric(
            "Pronóstico 6 meses",
            f"{close_rate_data['predicted_6m']:.1%}",
            delta=f"{(close_rate_data['predicted_6m'] - close_rate_data['current_rate']) * 100:.1f}%"
        )
    with col3:
        st.metric(
            "Total Leads",
            len(df),
            delta=f"{df['closed'].sum()} cerrados"
        )
    
    st.plotly_chart(close_rate_data["chart"], use_container_width=True, key="overview_close_rate")


def _render_seller_close_rate(df: pd.DataFrame) -> None:
    """Renderiza la métrica de tasa de cierre por vendedor."""
    st.subheader("Tasa de Cierre por Vendedor")
    
    seller_data = calculate_close_rate_by_seller(df)
    
    render_chart_with_expander(
        chart_fig=seller_data["chart"],
        expander_title="📊 Ver tabla detallada",
        expander_df=seller_data["seller_stats"],
        df_format={
            "close_rate": "{:.1%}",
            "closed_count": "{:.0f}",
            "total": "{:.0f}"
        }
    )


def _render_lead_potential_index(df: pd.DataFrame) -> None:
    """Renderiza el índice de potencial de lead."""
    st.subheader("Índice de Potencial de Lead")
    
    lead_potential_data = calculate_lead_potential_index(df)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.plotly_chart(
            lead_potential_data["chart"],
            use_container_width=True,
            key="overview_lead_potential_gauge"
        )
    
    with col2:
        st.markdown("**Top 10 Leads con Mayor Potencial**")
        st.dataframe(
            lead_potential_data["top_leads"].style.format({
                "lead_score": "{:.1f}",
                "closed": lambda x: "✅ Cerrado" if x == 1 else "❌ Abierto"
            }).background_gradient(subset=["lead_score"], cmap="RdYlGn", vmin=0, vmax=100),
            use_container_width=True,
            height=400
        )


def _render_volume_distribution(df: pd.DataFrame) -> None:
    """Renderiza la distribución de volumen numérico."""
    st.subheader("Distribución de Volumen Numérico")
    vol_chart = calculate_volume_distribution(df)
    st.plotly_chart(vol_chart, use_container_width=True, key="overview_volume_dist")


def _render_upsell_opportunities(df: pd.DataFrame) -> None:
    """Renderiza las oportunidades de upsell en radar."""
    st.subheader("Oportunidades de Upsell")
    upsell_chart = calculate_upsell_radar(df)
    st.plotly_chart(upsell_chart, use_container_width=True, key="overview_upsell_radar")
