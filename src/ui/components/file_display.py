"""
Visualización de resúmenes y previsualizaciones de archivos.
"""

import streamlit as st
import pandas as pd


def display_file_summary(summary: dict, df: pd.DataFrame, compact: bool = False) -> None:
    """
    Muestra un resumen de los datos validados.
    
    Args:
        summary: Diccionario con resumen de validación
        df: DataFrame normalizado
        compact: Si es True, usa layout compacto para sidebar
    """
    st.success("✅ Archivo validado correctamente")
    
    if compact:
        _display_compact_summary(summary)
    else:
        _display_full_summary(summary)
    
    _display_preview(df, compact)


def _display_compact_summary(summary: dict) -> None:
    """Muestra resumen compacto (para sidebar)."""
    st.metric("📊 Total de registros", summary["total_rows"])
    st.metric("✅ Reuniones cerradas", summary["closed_count"])
    st.metric("📂 Reuniones abiertas", summary["open_count"])
    
    st.markdown("---")
    st.markdown(f"**📅 Fechas:** {summary['date_range']['min']} → {summary['date_range']['max']}")
    
    if summary["sellers"]:
        sellers_list = summary['sellers']
        if len(sellers_list) <= 2:
            st.markdown(f"**👤 Vendedores:** {', '.join(sellers_list)}")
        else:
            st.markdown(f"**👤 Vendedores:** {', '.join(sellers_list[:2])} (+{len(sellers_list)-2})")


def _display_full_summary(summary: dict) -> None:
    """Muestra resumen completo (para página principal)."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total de registros", summary["total_rows"])
    
    with col2:
        st.metric("✅ Reuniones cerradas", summary["closed_count"])
    
    with col3:
        st.metric("📂 Reuniones abiertas", summary["open_count"])
    
    with col4:
        st.metric("👥 Vendedores", summary["unique_sellers"])
    
    st.markdown("")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown(f"**📅 Rango de fechas:** {summary['date_range']['min']} → {summary['date_range']['max']}")
    
    with info_col2:
        if summary["sellers"]:
            sellers_text = ", ".join(summary['sellers'][:3])
            if len(summary['sellers']) > 3:
                sellers_text += f" (+{len(summary['sellers']) - 3} más)"
            st.markdown(f"**👤 Vendedores:** {sellers_text}")


def _display_preview(df: pd.DataFrame, compact: bool) -> None:
    """Muestra vista previa de los datos."""
    expander_label = "Vista previa" if compact else "Vista previa de los datos (primeras 10 filas)"
    with st.expander(expander_label):
        st.dataframe(
            df[["Nombre", "Correo Electronico", "Fecha de la Reunion", "Vendedor asignado", "closed"]].head(10),
            use_container_width=True,
            hide_index=True
        )
