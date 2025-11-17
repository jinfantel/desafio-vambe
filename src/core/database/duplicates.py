"""
Verificación de duplicados en la base de datos.
"""

import sqlite3
import pandas as pd
from typing import Tuple, Set

from .config import DB_PATH
from .utils import db_exists_and_has_data


def get_existing_keys() -> Set[Tuple[str, str, str]]:
    """
    Obtiene todas las claves únicas (client_name, email, fecha) existentes en la DB.
    
    Returns:
        Set de tuplas (client_name, correo_electronico, fecha_reunion)
    """
    if not db_exists_and_has_data():
        return set()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT client_name, correo_electronico, fecha_reunion
        FROM clients
    """)
    existing_records = set(cursor.fetchall())
    conn.close()
    
    return existing_records


def check_duplicates(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """
    Verifica qué registros del DataFrame ya existen en la base de datos.
    
    Args:
        df: DataFrame con nuevos datos a verificar
        
    Returns:
        Tupla con (df_no_duplicados, cantidad_duplicados)
    """
    existing_records = get_existing_keys()
    
    if not existing_records:
        return df, 0
    
    mask = []
    for _, row in df.iterrows():
        client_name = row.get('Nombre', row.get('client_name'))
        correo = row.get('Correo Electronico', '')
        fecha = str(row.get('Fecha de la Reunion', ''))
        
        unique_key = (client_name, correo, fecha)
        is_duplicate = unique_key in existing_records
        mask.append(not is_duplicate)
    
    df_no_duplicados = df[mask].copy()
    duplicados = len(df) - len(df_no_duplicados)
    
    return df_no_duplicados, duplicados
