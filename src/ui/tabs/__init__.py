"""
Pestañas del dashboard - Módulos individuales.
"""

from .overview import render_overview_tab
from .deep_analysis import render_deep_analysis_tab
from .hot_leads import render_hot_leads_tab
from .concerns import render_concerns_tab

__all__ = [
    'render_overview_tab',
    'render_deep_analysis_tab',
    'render_hot_leads_tab',
    'render_concerns_tab'
]
