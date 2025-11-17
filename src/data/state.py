"""
Manejo de estado de sesión.
"""

import streamlit as st
import pandas as pd


def initialize_session_state_from_db(df: pd.DataFrame) -> None:
    """
    Inicializa el session state cuando se carga desde DB.
    
    Args:
        df: DataFrame cargado desde la base de datos
    """
    st.session_state.categorized = True
    st.session_state.df_categorized = df
