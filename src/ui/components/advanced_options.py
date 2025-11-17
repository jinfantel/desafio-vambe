"""
Opciones avanzadas del sidebar.
"""

import streamlit as st

from src.core.ai import clear_categorization_cache
from src.core.database import delete_database


def render_advanced_options() -> None:
    """Renderiza el expander de opciones avanzadas con reprocesamiento y caché."""
    with st.expander("⚙️ Opciones Avanzadas"):
        st.caption("**Reprocesar todo:** Borra la base de datos y vuelve a categorizar las transcripciones con Gemini.")
        
        if st.button("Reprocesar Todo", type="primary", use_container_width=True, key="btn_reprocess"):
            st.session_state.confirm_reprocess = True
        
        if st.button("Limpiar Caché", type="secondary", use_container_width=True, key="btn_clear_cache"):
            clear_categorization_cache()
        
        if st.session_state.get("confirm_reprocess", False):
            _handle_reprocess_confirmation()


def _handle_reprocess_confirmation() -> None:
    """Maneja la confirmación de reprocesamiento con botones de confirmación."""
    st.warning("⚠️ **¿Estás seguro?** Esto borrará todos los datos procesados para llamar nuevamente a Gemini API.")
    
    if st.button("✅ Sí, Reprocesar", type="primary", use_container_width=True, key="confirm_yes"):
        _execute_reprocess()
    
    if st.button("❌ Cancelar", use_container_width=True, key="confirm_no"):
        _cancel_reprocess()


def _execute_reprocess() -> None:
    """Ejecuta el reprocesamiento completo."""
    if delete_database():
        st.success("✅ Base de datos eliminada")
    
    clear_categorization_cache()
    
    st.session_state.categorized = False
    st.session_state.categorizing = False
    st.session_state.confirm_reprocess = False
    if "df_categorized" in st.session_state:
        del st.session_state.df_categorized
    
    st.rerun()


def _cancel_reprocess() -> None:
    """Cancela el reprocesamiento."""
    st.session_state.confirm_reprocess = False
    st.rerun()
