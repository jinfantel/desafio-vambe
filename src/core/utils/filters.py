"""
Funciones de filtrado de DataFrames.
"""

import pandas as pd
from typing import List, Optional
from datetime import datetime


def filter_dataframe(
    df: pd.DataFrame,
    vendedor: Optional[List[str]] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    sector: Optional[List[str]] = None,
    fuente: Optional[List[str]] = None,
    volumen_nivel: Optional[List[str]] = None,
    urgencia: Optional[List[str]] = None,
    search_text: Optional[str] = None
) -> pd.DataFrame:
    """
    Filtra el DataFrame según múltiples criterios.
    
    Args:
        df: DataFrame a filtrar
        vendedor: Lista de vendedores a incluir
        fecha_inicio: Fecha de inicio del rango
        fecha_fin: Fecha fin del rango
        sector: Lista de sectores a incluir
        fuente: Lista de fuentes a incluir
        volumen_nivel: Lista de niveles de volumen a incluir
        urgencia: Lista de niveles de urgencia a incluir
        search_text: Texto a buscar en transcripciones
        
    Returns:
        DataFrame filtrado
    """
    filtered_df = df.copy()
    
    if vendedor and len(vendedor) > 0:
        filtered_df = filtered_df[filtered_df["Vendedor asignado"].isin(vendedor)]
    
    if fecha_inicio and fecha_fin:
        fecha_col = pd.to_datetime(filtered_df["Fecha de la Reunion"])
        filtered_df = filtered_df[
            (fecha_col >= pd.to_datetime(fecha_inicio)) & 
            (fecha_col <= pd.to_datetime(fecha_fin))
        ]
    
    if sector and len(sector) > 0 and "sector_principal" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["sector_principal"].isin(sector)]
    
    if fuente and len(fuente) > 0 and "fuente_primaria" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["fuente_primaria"].isin(fuente)]
    
    if volumen_nivel and len(volumen_nivel) > 0 and "volumen_nivel" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["volumen_nivel"].isin(volumen_nivel)]
    
    if urgencia and len(urgencia) > 0 and "urgencia_nivel" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["urgencia_nivel"].isin(urgencia)]
    
    if search_text and len(search_text) > 0:
        search_text = search_text.lower()
        mask = (
            filtered_df["Transcripcion"].str.lower().str.contains(search_text, na=False) |
            filtered_df["Nombre"].str.lower().str.contains(search_text, na=False)
        )
        if "preocupaciones_texto" in filtered_df.columns:
            mask = mask | filtered_df["preocupaciones_texto"].str.lower().str.contains(search_text, na=False)
        
        filtered_df = filtered_df[mask]
    
    return filtered_df
