"""
Filtros del sidebar - Componentes reutilizables.
"""

import streamlit as st
import pandas as pd
from typing import List, Tuple
from datetime import date


def render_date_filters(df: pd.DataFrame) -> Tuple[date, date]:
    """
    Renderiza los filtros de rango de fechas.
    
    Args:
        df: DataFrame con columna "Fecha de la Reunion"
        
    Returns:
        Tupla (fecha_inicio, fecha_fin)
    """
    min_date = df["Fecha de la Reunion"].min()
    max_date = df["Fecha de la Reunion"].max()
    
    fecha_inicio = st.date_input(
        "Fecha inicio",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )
    
    fecha_fin = st.date_input(
        "Fecha fin",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )
    
    return fecha_inicio, fecha_fin


def render_categorical_filters(df: pd.DataFrame) -> dict:
    """
    Renderiza todos los filtros categóricos.
    
    Args:
        df: DataFrame con los datos
        
    Returns:
        Dict con las selecciones: {
            'sectores': List[str],
            'fuentes': List[str],
            'volumenes': List[str],
            'urgencias': List[str]
        }
    """
    filters = {}
    
    if "sector_principal" in df.columns:
        sectores = df["sector_principal"].dropna().unique().tolist()
        filters['sectores'] = st.multiselect(
            "Sector Principal",
            options=sorted(sectores),
            default=[]
        )
    else:
        filters['sectores'] = []
    
    if "fuente_primaria" in df.columns:
        fuentes = df["fuente_primaria"].dropna().unique().tolist()
        filters['fuentes'] = st.multiselect(
            "Fuente de Descubrimiento",
            options=sorted(fuentes),
            default=[]
        )
    else:
        filters['fuentes'] = []
    
    if "volumen_nivel" in df.columns:
        volumenes = df["volumen_nivel"].dropna().unique().tolist()
        filters['volumenes'] = st.multiselect(
            "Nivel de Volumen",
            options=sorted(volumenes),
            default=[]
        )
    else:
        filters['volumenes'] = []
    
    if "urgencia_nivel" in df.columns:
        urgencias = df["urgencia_nivel"].dropna().unique().tolist()
        filters['urgencias'] = st.multiselect(
            "Urgencia",
            options=sorted(urgencias),
            default=[]
        )
    else:
        filters['urgencias'] = []
    
    return filters


def render_search_filter() -> str:
    """
    Renderiza el filtro de búsqueda de texto.
    
    Returns:
        Texto de búsqueda ingresado
    """
    return st.text_input(
        "🔎 Buscar en transcripciones",
        placeholder="Ej: integración, confidencialidad..."
    )
