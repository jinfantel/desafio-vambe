"""
Módulo de base de datos SQLite para persistir categorizaciones.
Funciona perfecto en deploy (Render/Railway) sin configuración adicional.

Estructura modular:
- crud.py: Operaciones básicas (save, load, append, delete)
- duplicates.py: Verificación de duplicados
- serialization.py: Conversión DataFrame ↔ DB records
- schema.py: Definición de tablas
- utils.py: Funciones auxiliares
- config.py: Configuración y rutas
"""

from .schema import init_database
from .crud import (
    save_processed_data,
    load_processed_data,
    append_processed_data,
    delete_database
)
from .duplicates import check_duplicates
from .utils import db_exists_and_has_data
from .config import DB_PATH

__all__ = [
    "init_database",
    "save_processed_data",
    "load_processed_data",
    "append_processed_data",
    "delete_database",
    "check_duplicates",
    "db_exists_and_has_data",
    "DB_PATH"
]
