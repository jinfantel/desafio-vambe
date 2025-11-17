"""
Componentes de visualización de leads.
"""

import streamlit as st
import pandas as pd
import json
from typing import List


def render_lead_table(
    df: pd.DataFrame,
    display_columns: List[str],
    format_dict: dict = None,
    height: int = 600,
    gradient_column: str = None
) -> None:
    """
    Renderiza una tabla de leads con formato.
    
    Args:
        df: DataFrame con los leads
        display_columns: Columnas a mostrar
        format_dict: Dict con formato de columnas
        height: Altura de la tabla
        gradient_column: Columna para aplicar gradiente de color
    """
    available_cols = [col for col in display_columns if col in df.columns]
    
    styled_df = df[available_cols].style
    
    if format_dict:
        styled_df = styled_df.format(format_dict)
    
    if gradient_column and gradient_column in available_cols:
        styled_df = styled_df.background_gradient(
            subset=[gradient_column],
            cmap="RdYlGn",
            vmin=0,
            vmax=100
        )
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=height
    )


def render_transcript_viewer(df: pd.DataFrame) -> None:
    """
    Renderiza el visor de transcripciones con selector de leads.
    
    Args:
        df: DataFrame con los leads (debe tener lead_score)
    """
    st.subheader("📄 Ver Transcripción Completa")
    
    selected_lead = st.selectbox(
        "Selecciona un lead:",
        df["Nombre"].tolist()
    )
    
    if selected_lead:
        lead_row = df[df["Nombre"] == selected_lead].iloc[0]
        
        if not lead_row.get("_categorization_success", True):
            st.warning("⚠️ **Categorización fallida**: Este lead tiene valores por defecto.")
        
        _render_lead_metrics(lead_row)
        
        st.markdown("**📝 Transcripción Completa:**")
        st.text_area(
            "Transcripción",
            lead_row["Transcripcion"],
            height=300,
            label_visibility="collapsed"
        )
        
        _render_lead_concerns(lead_row)


def _render_lead_metrics(lead_row: pd.Series) -> None:
    """Renderiza las métricas principales del lead."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = lead_row.get('lead_score', 0)
        st.metric("Lead Score", f"{score:.1f}/100")
    
    with col2:
        status = "✅ Cerrado" if lead_row["closed"] == 1 else "❌ No Cerrado"
        st.metric("Status", status)
    
    with col3:
        st.metric("Vendedor", lead_row["Vendedor asignado"])


def _render_lead_concerns(lead_row: pd.Series) -> None:
    """Renderiza las preocupaciones de un lead."""
    if "preocupaciones" not in lead_row:
        return
    
    try:
        preocupaciones_data = lead_row["preocupaciones"]
        
        if isinstance(preocupaciones_data, str):
            preocupaciones_list = json.loads(preocupaciones_data)
        else:
            preocupaciones_list = preocupaciones_data if isinstance(preocupaciones_data, list) else []
        
        if preocupaciones_list:
            st.markdown("**⚠️ Preocupaciones Detectadas:**")
            for concern in preocupaciones_list:
                if isinstance(concern, dict):
                    st.warning(
                        f"**{concern.get('tipo', 'N/A')}** (Impacto: {concern.get('impacto', 'N/A')})\n\n"
                        f"_{concern.get('ejemplo_frase', 'N/A')}_"
                    )
    except (json.JSONDecodeError, Exception):
        pass
