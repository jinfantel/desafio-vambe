"""
Componente Sidebar - Filtros y opciones de configuración.
Versión refactorizada usando componentes modulares.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any

from src.core.utils import filter_dataframe
from .components import (
    render_date_filters,
    render_categorical_filters,
    render_search_filter,
    render_advanced_options,
    render_file_uploader
)


def render_sidebar(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Renderiza el sidebar con filtros y opciones avanzadas.
    
    Args:
        df: DataFrame con los datos
        
    Returns:
        Dict con los filtros seleccionados
    """
    with st.sidebar:
        st.title("📊 Vambe Analytics")
        st.markdown("---")
        
        st.header("🔍 Filtros")
        
        vendedor_col = "Vendedor asignado"
        vendedores_disponibles = sorted(df[vendedor_col].dropna().unique().tolist())
        vendedores_selected = st.multiselect(
            "Vendedor",
            options=vendedores_disponibles,
            default=[]
        )
        
        fecha_inicio, fecha_fin = render_date_filters(df)
        
        categorical_filters = render_categorical_filters(df)
        
        st.markdown("---")
        
        search_text = render_search_filter()
        
        st.markdown("---")
        
        render_advanced_options()
        
        st.markdown("---")
        
        with st.expander("📤 Cargar Más Datos", expanded=False):
            render_file_uploader()
        
        st.markdown("---")
        
        _render_failed_categorizations_indicator(df)
    
    return {
        "vendedores": vendedores_selected if vendedores_selected else None,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "sectores": categorical_filters['sectores'] if categorical_filters['sectores'] else None,
        "fuentes": categorical_filters['fuentes'] if categorical_filters['fuentes'] else None,
        "volumenes": categorical_filters['volumenes'] if categorical_filters['volumenes'] else None,
        "urgencias": categorical_filters['urgencias'] if categorical_filters['urgencias'] else None,
        "search_text": search_text if search_text else None
    }


def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Aplica los filtros seleccionados al DataFrame.
    
    Args:
        df: DataFrame original
        filters: Dict con los filtros (output de render_sidebar)
        
    Returns:
        DataFrame filtrado
    """
    return filter_dataframe(
        df=df,
        vendedor=filters["vendedores"],
        fecha_inicio=filters["fecha_inicio"],
        fecha_fin=filters["fecha_fin"],
        sector=filters["sectores"],
        fuente=filters["fuentes"],
        volumen_nivel=filters["volumenes"],
        urgencia=filters["urgencias"],
        search_text=filters["search_text"]
    )


def _render_failed_categorizations_indicator(df: pd.DataFrame) -> None:
    """Muestra indicador de categorizaciones fallidas si existen."""
    if "_categorization_success" in df.columns:
        failed_count = (~df["_categorization_success"]).sum()
        if failed_count > 0:
            st.error(f"⚠️ **{int(failed_count)} leads** con categorización fallida")
            st.caption("Estos leads tienen valores por defecto. Considera reprocesarlos.")
