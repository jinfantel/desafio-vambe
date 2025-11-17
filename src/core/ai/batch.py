"""
Procesamiento en batch de transcripciones.
"""

import time
from typing import Dict, Any, List, Optional, Callable

import streamlit as st

from .client import call_gemini_batch_api
from .prompts import build_batch_categorization_prompt
from .defaults import (
    BATCH_SIZE,
    RETRY_ATTEMPTS,
    RATE_LIMIT_DELAY,
    get_default_categorization
)


def process_batch(
    batch_transcripts: List[str],
    batch_names: List[str],
    batch_start: int
) -> List[Dict[str, Any]]:
    """
    Procesa un grupo de transcripciones con retry automático.
    
    Args:
        batch_transcripts: Transcripciones del grupo
        batch_names: Nombres del grupo
        batch_start: Índice de inicio del grupo
        
    Returns:
        Lista de resultados para el grupo
    """
    batch_size = len(batch_transcripts)
    prompt = build_batch_categorization_prompt(
        batch_transcripts, 
        batch_names, 
        batch_start, 
        batch_size
    )
    
    for attempt in range(RETRY_ATTEMPTS):
        try:
            if attempt > 0:
                time.sleep(2 ** attempt)  # Exponential backoff
            
            batch_results = call_gemini_batch_api(prompt, batch_size)
            
            for result in batch_results:
                result["_categorization_success"] = True
            
            return batch_results
        
        except Exception as e:
            error_msg = str(e)
            
            if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                st.error(f"❌ Límite de API alcanzado en batch {batch_start+1}-{batch_start+batch_size}")
                st.info("💡 Espera unos minutos o verifica tu cuota en Google AI Studio")
                return [get_default_categorization() for _ in range(batch_size)]
            
            if attempt == RETRY_ATTEMPTS - 1:
                st.warning(f"⚠️ Error en grupo {batch_start+1}-{batch_start+batch_size}: {error_msg[:100]}")
    
    # Si falla después de todos los intentos, usar valores por defecto
    return [get_default_categorization() for _ in range(batch_size)]


def batch_categorize_with_progress(
    transcripts: List[str],
    client_names: List[str],
    progress_callback: Optional[Callable] = None
) -> List[Dict[str, Any]]:
    """
    Categoriza múltiples transcripciones en grupos con actualización de progreso.
    
    Args:
        transcripts: Lista de transcripciones
        client_names: Lista de nombres de clientes
        progress_callback: Función opcional para actualizar progreso
        
    Returns:
        Lista de diccionarios con categorías
    """
    total = len(transcripts)
    results = []
    failed_count = 0
    
    for batch_start in range(0, total, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total)
        batch_results = process_batch(
            transcripts[batch_start:batch_end],
            client_names[batch_start:batch_end],
            batch_start
        )
        
        results.extend(batch_results)
        
        failed_count += sum(1 for r in batch_results if not r.get("_categorization_success", True))
        
        if progress_callback:
            progress_callback(batch_end, total)
        
        if batch_end < total:
            time.sleep(RATE_LIMIT_DELAY)
    
    return results