"""
Funciones de utilidad para la base de datos.
"""

import sqlite3
from .config import DB_PATH


def db_exists_and_has_data() -> bool:
    """
    Verifica si la base de datos existe y tiene datos.
    
    Returns:
        True si existe y tiene al menos 1 registro
    """
    if not DB_PATH.exists():
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clients")
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except Exception:
        return False
