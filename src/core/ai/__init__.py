"""
Categorizador de transcripciones usando Google Gemini API con structured outputs.
Utiliza caching para evitar llamadas repetidas a la API.

Módulos:
- config: Configuración de la API de Gemini
- defaults: Valores por defecto y constantes
- prompts: Construcción de prompts
- api: Llamadas a la API de Gemini
- single: Categorización individual con caché
- batch: Procesamiento en batch optimizado
- cache: Gestión del caché

Funciones públicas exportadas:
- configure_gemini(): Configura la API key
- categorize_transcript(): Categoriza una sola transcripción (con caché)
- batch_categorize_transcripts(): Categoriza múltiples en grupos de 5 (optimizado)
- clear_categorization_cache(): Limpia el caché de categorizaciones
"""

from typing import Dict, Any, List, Optional, Callable

import streamlit as st

from .config import configure_gemini
from .single import categorize_single_transcript
from .batch import batch_categorize_with_progress
from .cache import clear_categorization_cache as _clear_cache


def categorize_transcript(transcript: str, client_name: str = "") -> Dict[str, Any]:
    """
    Categoriza una transcripción usando Gemini con structured output (JSON Schema).
    
    Los resultados se cachean automáticamente para evitar llamadas repetidas.
    
    Args:
        transcript: Texto de la transcripción a categorizar
        client_name: Nombre del cliente (para contexto adicional)
        
    Returns:
        Dict con las categorías extraídas según CATEGORIZATION_SCHEMA
        
    Note:
        Esta función es principalmente para uso individual. Para procesar múltiples
        transcripciones, usar batch_categorize_transcripts() que es más eficiente.
    """
    return categorize_single_transcript(transcript, client_name)


def batch_categorize_transcripts(
    transcripts: List[str],
    client_names: List[str],
    _progress_callback: Optional[Callable] = None
) -> List[Dict[str, Any]]:
    """
    Categoriza múltiples transcripciones en GRUPOS DE 5 usando una sola llamada API por grupo.
    Esto reduce drásticamente el uso de tokens y llamadas a la API.
    
    Args:
        transcripts: Lista de transcripciones
        client_names: Lista de nombres de clientes
        _progress_callback: Función opcional para actualizar progreso
        
    Returns:
        Lista de diccionarios con categorías
        
    Note:
        - Procesa en grupos de 5 para optimizar costos
        - Implementa retry con exponential backoff
        - Usa valores por defecto si falla después de 3 intentos
        - NO usa cache para permitir callbacks de progreso de Streamlit
    """
    return batch_categorize_with_progress(transcripts, client_names, _progress_callback)


def clear_categorization_cache() -> None:
    """
    Limpia el caché de categorizaciones.
    Útil cuando se quiere forzar una re-categorización.
    
    Note:
        batch_categorize_transcripts no usa cache (para compatibilidad con Streamlit),
        solo limpia el cache de categorize_single_transcript.
    """
    categorize_single_transcript.clear()
    _clear_cache()


__all__ = [
    "configure_gemini",
    "categorize_transcript",
    "batch_categorize_transcripts",
    "clear_categorization_cache",
]
