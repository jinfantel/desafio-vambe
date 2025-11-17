"""
Módulo de tasa de cierre.
Exporta las funciones públicas para mantener compatibilidad.
"""

from .metrics import (
    calculate_global_close_rate,
    calculate_close_rate_by_seller,
    calculate_close_heatmap
)

__all__ = [
    "calculate_global_close_rate",
    "calculate_close_rate_by_seller",
    "calculate_close_heatmap"
]
