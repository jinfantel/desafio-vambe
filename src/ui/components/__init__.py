"""
Componentes UI - Módulos de interfaz modularizados.

Estructura:
- filters.py: Todos los filtros del sidebar
- advanced_options.py: Opciones avanzadas
- metrics_display.py: Display de métricas individuales
- lead_viewer.py: Visualización de leads
- concerns_display.py: Display de preocupaciones
- file_uploader.py: Carga de datos adicionales
- initial_uploader.py: Carga inicial de datos (pantalla principal)
"""

from .filters import (
    render_date_filters,
    render_categorical_filters,
    render_search_filter
)
from .advanced_options import render_advanced_options
from .metrics_display import (
    render_metric_card,
    render_metrics_grid,
    render_chart_with_expander
)
from .lead_viewer import (
    render_lead_table,
    render_transcript_viewer
)
from .concerns_display import (
    render_concerns_table,
    render_concerns_explorer
)
from .file_uploader import render_file_uploader
from .initial_uploader import render_initial_uploader

__all__ = [
    'render_date_filters',
    'render_categorical_filters',
    'render_search_filter',
    'render_advanced_options',
    'render_metric_card',
    'render_metrics_grid',
    'render_lead_table',
    'render_transcript_viewer',
    'render_concerns_table',
    'render_concerns_explorer',
    'render_file_uploader',
    'render_initial_uploader'
]
