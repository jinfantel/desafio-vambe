"""
Componentes de display de preocupaciones.
"""

import streamlit as st
import pandas as pd


def render_concerns_table(concerns_df: pd.DataFrame) -> None:
    """
    Renderiza la tabla de resumen de preocupaciones.
    
    Args:
        concerns_df: DataFrame con las preocupaciones expandidas
    """
    st.subheader("📊 Desglose Completo de Preocupaciones")
    
    concern_summary = concerns_df.groupby("tipo").agg({
        "closed": ["count", "sum", "mean"]
    }).reset_index()
    
    concern_summary.columns = ["Tipo", "Total Menciones", "Cerrados", "Tasa Cierre"]
    concern_summary = concern_summary.sort_values("Total Menciones", ascending=False)
    
    st.dataframe(
        concern_summary.style.format({
            "Tasa Cierre": "{:.1%}",
            "Total Menciones": "{:.0f}",
            "Cerrados": "{:.0f}"
        }).background_gradient(subset=["Tasa Cierre"], cmap="RdYlGn"),
        use_container_width=True
    )
    
    return concern_summary


def render_concerns_explorer(df: pd.DataFrame, concerns_df: pd.DataFrame) -> None:
    """
    Renderiza el explorador interactivo de leads por preocupación.
    
    Args:
        df: DataFrame principal con todos los leads
        concerns_df: DataFrame con las preocupaciones expandidas
    """
    st.subheader("🔍 Explorar Leads por Preocupación")
    
    concern_summary = concerns_df.groupby("tipo").agg({
        "closed": ["count"]
    }).reset_index()
    concern_summary.columns = ["Tipo", "Total"]
    concern_summary = concern_summary.sort_values("Total", ascending=False)
    
    concern_type = st.selectbox(
        "Selecciona un tipo de preocupación:",
        concern_summary["Tipo"].tolist()
    )
    
    if concern_type:
        _render_leads_with_concern(df, concerns_df, concern_type)


def _render_leads_with_concern(
    df: pd.DataFrame,
    concerns_df: pd.DataFrame,
    concern_type: str
) -> None:
    """
    Renderiza los leads que tienen una preocupación específica.
    
    Args:
        df: DataFrame principal
        concerns_df: DataFrame de preocupaciones
        concern_type: Tipo de preocupación a filtrar
    """
    leads_with_concern = concerns_df[concerns_df["tipo"] == concern_type]["nombre"].unique()
    
    st.markdown(f"**{len(leads_with_concern)} leads mencionaron '{concern_type}':**")
    
    for name in leads_with_concern[:10]:
        lead_info = df[df["Nombre"] == name].iloc[0]
        
        with st.expander(
            f"{'✅' if lead_info['closed'] == 1 else '❌'} {name} - {lead_info['Vendedor asignado']}"
        ):
            _render_lead_detail(lead_info, name, concern_type)


def _render_lead_detail(lead_info: pd.Series, name: str, concern_type: str) -> None:
    """Renderiza el detalle de un lead específico."""
    st.write(f"**Fecha:** {lead_info['Fecha de la Reunion'].strftime('%Y-%m-%d')}")
    st.write(f"**Sector:** {lead_info.get('sector_principal', 'N/A')}")
    st.write(f"**Volumen:** {lead_info.get('volumen_nivel', 'N/A')}")
    st.write(f"**Urgencia:** {lead_info.get('urgencia_nivel', 'N/A')}")
    
    st.markdown("**Transcripción completa:**")
    st.text_area(
        "Transcripción",
        value=lead_info["Transcripcion"],
        height=300,
        disabled=True,
        label_visibility="collapsed",
        key=f"transcript_{name}_{concern_type}"
    )
