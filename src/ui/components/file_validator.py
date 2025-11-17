"""
Validación y normalización de archivos subidos.
"""

import streamlit as st
import pandas as pd
from typing import Optional

from src.data.validation import validate_dataframe_schema, normalize_dataframe
from .file_reader import read_uploaded_file


def validate_and_normalize_file(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Lee, valida y normaliza un archivo subido.
    
    Args:
        uploaded_file: Archivo subido por Streamlit
        
    Returns:
        DataFrame normalizado o None si hay error
    """
    df = read_uploaded_file(uploaded_file)
    
    if df is None:
        st.error("❌ Error al leer el archivo. Verifica el formato.")
        return None
    
    is_valid, errors = validate_dataframe_schema(df)
    
    if not is_valid:
        st.error("❌ El archivo no cumple con la estructura requerida:")
        for error in errors:
            st.error(f"  • {error}")
        return None
    
    return normalize_dataframe(df)
