"""
Operaciones CRUD básicas para la base de datos SQLite.
"""

import sqlite3
import pandas as pd
from typing import Optional

from .config import DB_PATH
from .schema import init_database
from .utils import db_exists_and_has_data
from .serialization import dataframe_to_records, records_to_dataframe
from .duplicates import check_duplicates


def save_processed_data(df: pd.DataFrame) -> None:
    """
    Guarda el DataFrame procesado (con categorías) en SQLite.
    Reemplaza todos los datos existentes.
    
    Args:
        df: DataFrame con todas las columnas del CSV + categorías
    """
    init_database()
    
    records = dataframe_to_records(df)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM clients")
    
    cursor.executemany("""
        INSERT INTO clients (
            client_name, correo_electronico, numero_telefono, fecha_reunion,
            vendedor_asignado, closed, transcript, sector_principal, sector_secundario,
            volumen_numerico, volumen_nivel, es_pico_estacional,
            fuente_primaria, fuente_detalle, preocupaciones,
            urgencia_nivel, potencial_upsell, categorization_success
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    
    conn.commit()
    conn.close()


def load_processed_data() -> Optional[pd.DataFrame]:
    """
    Carga los datos procesados desde SQLite.
    
    Returns:
        DataFrame con todos los datos en el formato esperado por la app, o None si no existe la DB
    """
    if not db_exists_and_has_data():
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        
        df_raw = pd.read_sql_query("""
            SELECT 
                client_name, correo_electronico, numero_telefono, fecha_reunion,
                vendedor_asignado, closed, transcript,
                sector_principal, sector_secundario,
                volumen_numerico, volumen_nivel, es_pico_estacional,
                fuente_primaria, fuente_detalle, preocupaciones,
                urgencia_nivel, potencial_upsell, categorization_success
            FROM clients
            ORDER BY id
        """, conn)
        
        conn.close()
        
        return records_to_dataframe(df_raw)
        
    except Exception as e:
        print(f"Error cargando datos desde DB: {e}")
        return None


def append_processed_data(df_new: pd.DataFrame) -> int:
    """
    Añade nuevos datos procesados a la base de datos existente.
    Verifica duplicados basándose en: nombre, correo y fecha de reunión.
    
    Args:
        df_new: DataFrame con nuevos datos procesados
        
    Returns:
        Número de filas añadidas (excluyendo duplicados)
    """
    init_database()
    
    df_filtrado, duplicates_count = check_duplicates(df_new)
    
    if len(df_filtrado) == 0:
        if duplicates_count > 0:
            print(f"⚠️ Se omitieron {duplicates_count} registros duplicados")
        return 0
    
    records = dataframe_to_records(df_filtrado)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.executemany("""
        INSERT INTO clients (
            client_name, correo_electronico, numero_telefono, fecha_reunion,
            vendedor_asignado, closed, transcript, sector_principal, sector_secundario,
            volumen_numerico, volumen_nivel, es_pico_estacional,
            fuente_primaria, fuente_detalle, preocupaciones,
            urgencia_nivel, potencial_upsell, categorization_success
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    
    rows_added = len(records)
    conn.commit()
    conn.close()
    
    if duplicates_count > 0:
        print(f"⚠️ Se omitieron {duplicates_count} registros duplicados")
    
    return rows_added


def delete_database() -> bool:
    """
    Elimina completamente la base de datos.
    
    Returns:
        True si se eliminó exitosamente
    """
    try:
        if DB_PATH.exists():
            DB_PATH.unlink()
        return True
    except Exception as e:
        print(f"Error eliminando DB: {e}")
        return False
