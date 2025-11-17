"""
Funciones helper para parsing de datos categorizados.
Centraliza la lógica de parsing de JSON y construcción de texto.
"""

import json
import pandas as pd
from typing import List, Dict, Any, Optional


def parse_json_field(data: Any) -> Optional[List[Dict[str, Any]]]:
    """
    Parse un campo que puede ser string JSON o lista directamente.
    
    Args:
        data: Dato que puede ser string JSON, lista, o None
        
    Returns:
        Lista parseada o None si hay error
    """
    if data is None or (isinstance(data, float) and pd.isna(data)):
        return None
    
    if isinstance(data, str):
        try:
            return json.loads(data)
        except (json.JSONDecodeError, Exception):
            return None
    
    if isinstance(data, list):
        return data
    
    return None


def build_preocupaciones_texto(preocupaciones: List[Dict[str, Any]]) -> str:
    """
    Construye texto concatenado de preocupaciones para búsqueda/análisis.
    
    Args:
        preocupaciones: Lista de diccionarios con preocupaciones
        
    Returns:
        String con tipo y ejemplo_frase concatenados
    """
    if not preocupaciones or not isinstance(preocupaciones, list):
        return ""
    
    return " ".join([
        f"{p.get('tipo', '')} {p.get('ejemplo_frase', '')}"
        for p in preocupaciones
        if isinstance(p, dict)
    ])
