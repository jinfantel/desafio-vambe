"""
Funciones de transformación de datos.
"""

import pandas as pd
from typing import List, Dict, Any

from src.core.utils import build_preocupaciones_texto


def expand_categories_to_dataframe(df: pd.DataFrame, categories: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Expande las categorías del LLM en columnas del DataFrame.
    
    Args:
        df: DataFrame original
        categories: Lista de diccionarios con categorías de Gemini
        
    Returns:
        DataFrame expandido con columnas de categorización
    """
    df_expanded = df.copy()
    
    new_columns = [
        "sector_principal", "sector_secundario", "volumen_numerico", 
        "volumen_nivel", "es_pico_estacional", "fuente_primaria", 
        "fuente_detalle", "preocupaciones", "urgencia_nivel", 
        "potencial_upsell", "preocupaciones_texto", "_categorization_success"
    ]
    for col in new_columns:
        if col not in df_expanded.columns:
            df_expanded[col] = None
    
    for i, (idx, cat) in enumerate(zip(df_expanded.index, categories)):
        df_expanded.at[idx, "_categorization_success"] = cat.get("_categorization_success", True)
        df_expanded.at[idx, "sector_principal"] = cat.get("sector_principal", "Otros")
        df_expanded.at[idx, "sector_secundario"] = cat.get("sector_secundario")
        df_expanded.at[idx, "volumen_numerico"] = cat.get("volumen_numerico")
        df_expanded.at[idx, "volumen_nivel"] = cat.get("volumen_nivel", "Desconocido")
        df_expanded.at[idx, "es_pico_estacional"] = cat.get("es_pico_estacional", False)
        df_expanded.at[idx, "fuente_primaria"] = cat.get("fuente_primaria", "Otro")
        df_expanded.at[idx, "fuente_detalle"] = cat.get("fuente_detalle", "")
        
        preocupaciones = cat.get("preocupaciones", [])
        df_expanded.at[idx, "preocupaciones"] = preocupaciones
        
        df_expanded.at[idx, "urgencia_nivel"] = cat.get("urgencia_nivel", "Media")
        
        potencial = cat.get("potencial_upsell", [])
        df_expanded.at[idx, "potencial_upsell"] = potencial
        
        df_expanded.at[idx, "preocupaciones_texto"] = build_preocupaciones_texto(preocupaciones)
    
    return df_expanded
