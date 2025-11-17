"""
Funciones compartidas para los componentes de carga de archivos.

DEPRECATED: Este módulo se mantiene por compatibilidad pero delega a módulos especializados:
- file_reader.py: Lectura de CSV/Excel
- file_validator.py: Validación y normalización
- ai_processor.py: Categorización con IA
- file_display.py: Visualización de resúmenes

Se recomienda importar directamente desde los módulos especializados.
"""

from .file_reader import read_uploaded_file
from .file_validator import validate_and_normalize_file
from .ai_processor import categorize_dataframe
from .file_display import display_file_summary

__all__ = [
    "read_uploaded_file",
    "validate_and_normalize_file",
    "categorize_dataframe",
    "display_file_summary"
]
