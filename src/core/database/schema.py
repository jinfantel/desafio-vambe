"""
Schema y funciones de inicialización de la base de datos.
"""

import sqlite3
from .config import DB_PATH


def init_database() -> None:
    """
    Inicializa la base de datos SQLite con la tabla clients.
    Crea el directorio data/ si no existe.
    """
    DB_PATH.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            correo_electronico TEXT,
            numero_telefono TEXT,
            fecha_reunion TEXT,
            vendedor_asignado TEXT,
            closed INTEGER,
            transcript TEXT NOT NULL,
            sector_principal TEXT,
            sector_secundario TEXT,
            volumen_numerico INTEGER,
            volumen_nivel TEXT,
            es_pico_estacional INTEGER,
            fuente_primaria TEXT,
            fuente_detalle TEXT,
            preocupaciones TEXT,
            urgencia_nivel TEXT,
            potencial_upsell TEXT,
            categorization_success INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
