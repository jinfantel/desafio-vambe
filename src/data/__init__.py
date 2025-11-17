"""
Módulo de carga y procesamiento de datos.
Maneja la lógica de carga desde SQLite y la categorización con Gemini AI.
"""

from .api import load_or_process_data, has_data
from .transformer import expand_categories_to_dataframe

__all__ = [
    "load_or_process_data",
    "has_data",
    "expand_categories_to_dataframe"
]
