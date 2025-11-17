"""
API principal para carga y procesamiento de datos.
"""

import pandas as pd
from typing import Optional

from src.core.database import load_processed_data, db_exists_and_has_data
from .state import initialize_session_state_from_db


def load_or_process_data() -> Optional[pd.DataFrame]:
    """
    Carga los datos desde SQLite o retorna None si no hay datos.
    
    Esta función maneja toda la lógica de carga de datos:
    1. Intenta cargar desde SQLite (instantáneo)
    2. Si no existe, retorna None para mostrar el uploader
    
    Returns:
        DataFrame con los datos procesados o None si no hay datos
    """
    df_from_db = load_processed_data()
    
    if df_from_db is not None:
        initialize_session_state_from_db(df_from_db)
        return df_from_db
    
    return None


def has_data() -> bool:
    """
    Verifica si hay datos cargados en la base de datos.
    
    Returns:
        True si hay datos, False si no
    """
    return db_exists_and_has_data()
