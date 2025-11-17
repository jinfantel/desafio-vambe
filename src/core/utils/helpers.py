"""
Funciones helper generales.
"""

import pandas as pd

from src.core.config import COLORS

from typing import Dict


def get_color_by_value(value: float, thresholds: Dict[str, float]) -> str:
    """
    Retorna un color basado en umbrales.
    
    Args:
        value: Valor a evaluar
        thresholds: Dict con keys 'low', 'medium', 'high' y sus límites
        
    Returns:
        Color hex string
    """
    if value >= thresholds.get("high", 0.8):
        return COLORS["success"]
    elif value >= thresholds.get("medium", 0.5):
        return COLORS["warning"]
    else:
        return COLORS["danger"]


def get_month_name_es(month: int) -> str:
    """
    Retorna el nombre del mes en español.
    
    Args:
        month: Número de mes (1-12)
        
    Returns:
        Nombre del mes en español
    """
    months = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    return months.get(month, "")
