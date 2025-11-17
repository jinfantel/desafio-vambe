"""
Módulo UI - Componentes de interfaz de usuario del dashboard.
Versión modularizada con componentes reutilizables.
"""

from .sidebar import render_sidebar, apply_filters
from .tabs import (
    render_overview_tab,
    render_deep_analysis_tab,
    render_hot_leads_tab,
    render_concerns_tab
)

__all__ = [
    'render_sidebar',
    'apply_filters',
    'render_overview_tab',
    'render_deep_analysis_tab',
    'render_hot_leads_tab',
    'render_concerns_tab'
]
