"""
Categorización individual de transcripciones.
"""

from typing import Dict, Any

import streamlit as st

from .client import call_gemini_api
from .prompts import build_single_categorization_prompt
from .defaults import get_default_categorization, CACHE_TTL


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def categorize_single_transcript(transcript: str, client_name: str = "") -> Dict[str, Any]:
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
    try:
        prompt = build_single_categorization_prompt(transcript, client_name)
        result = call_gemini_api(prompt)
        result["_categorization_success"] = True
        return result
    
    except Exception as e:
        st.warning(f"⚠️ Error al categorizar {client_name}: {str(e)[:100]}")
        return get_default_categorization()
