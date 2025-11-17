"""
Configuración central para la aplicación Vambe Analytics Dashboard.
Este módulo re-exporta todas las configuraciones desde submódulos especializados.
"""

from .schema import CATEGORIZATION_SCHEMA
from .colors import COLORS
from .constants import VOLUMEN_SCORE_MAP, URGENCIA_SCORE_MAP
from .styles import CUSTOM_CSS
from ..ai.config import GEMINI_API_KEY, GEMINI_MODEL

__all__ = [
    "GEMINI_API_KEY",
    "GEMINI_MODEL",
    
    "CATEGORIZATION_SCHEMA",
    
    "COLORS",
    
    "VOLUMEN_SCORE_MAP",
    "URGENCIA_SCORE_MAP",
    
    "CUSTOM_CSS",
]
