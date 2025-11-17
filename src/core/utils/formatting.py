"""
Funciones de formateo y visualización.
"""

import pandas as pd


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Formatea un valor decimal como porcentaje.
    
    Args:
        value: Valor entre 0 y 1
        decimals: Cantidad de decimales
        
    Returns:
        String formateado (ej: "75.5%")
    """
    return f"{value * 100:.{decimals}f}%"


def format_number(value: float, decimals: int = 0) -> str:
    """
    Formatea un número con separadores de miles.
    
    Args:
        value: Número a formatear
        decimals: Cantidad de decimales
        
    Returns:
        String formateado (ej: "1,234")
    """
    return f"{value:,.{decimals}f}"


def clean_transcript_for_display(text: str, max_length: int = 200) -> str:
    """
    Limpia y trunca transcripción para mostrar en UI.
    
    Args:
        text: Transcripción completa
        max_length: Longitud máxima
        
    Returns:
        Texto limpio y truncado
    """
    if not text or pd.isna(text):
        return "Sin transcripción"
    
    text = " ".join(text.split())
    
    if len(text) > max_length:
        return text[:max_length] + "..."
    
    return text
