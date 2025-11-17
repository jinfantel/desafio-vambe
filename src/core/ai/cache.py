"""
Gestión del caché de categorizaciones.
"""

import streamlit as st

from .single import categorize_single_transcript


def clear_categorization_cache() -> None:
    """
    Limpia el caché de categorizaciones.
    Útil cuando se quiere forzar una re-categorización.
    """
    categorize_single_transcript.clear()
    st.success("✅ Caché limpio")
