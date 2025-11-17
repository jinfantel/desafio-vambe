"""
Lectura de archivos CSV y Excel.
"""

import streamlit as st
import pandas as pd
from typing import Optional


def read_uploaded_file(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Lee un archivo subido (CSV o Excel).
    
    Args:
        uploaded_file: Archivo subido por Streamlit
        
    Returns:
        DataFrame con los datos o None si hay error
    """
    try:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        if file_extension == "csv":
            try:
                return pd.read_csv(uploaded_file)
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                return pd.read_csv(uploaded_file, encoding="latin-1")
        
        elif file_extension in ["xlsx", "xls"]:
            return pd.read_excel(uploaded_file)
        
        return None
        
    except Exception as e:
        st.error(f"Error al leer archivo: {str(e)}")
        return None
