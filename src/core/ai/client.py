"""
Llamadas a la API de Google Gemini.
"""

import json
import re
from typing import Dict, Any, List

import google.generativeai as genai

from .config import get_gemini_model_name
from .defaults import SINGLE_TIMEOUT, BATCH_TIMEOUT


def call_gemini_api(prompt: str, timeout: int = SINGLE_TIMEOUT) -> Dict[str, Any]:
    """
    Realiza una llamada a la API de Gemini para una sola categorización.
    
    Args:
        prompt: Prompt construido
        timeout: Timeout en segundos
        
    Returns:
        Dict con el resultado parseado
        
    Raises:
        Exception: Si hay error en la llamada a la API
    """
    model = genai.GenerativeModel(
        model_name=get_gemini_model_name(),
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.1,
        }
    )
    
    response = model.generate_content(prompt, request_options={"timeout": timeout})
    return parse_json_response(response.text)


def call_gemini_batch_api(prompt: str, expected_size: int, timeout: int = BATCH_TIMEOUT) -> List[Dict[str, Any]]:
    """
    Realiza una llamada a la API de Gemini para un batch.
    
    Args:
        prompt: Prompt construido
        expected_size: Cantidad esperada de resultados
        timeout: Timeout en segundos
        
    Returns:
        Lista de dicts con resultados
        
    Raises:
        ValueError: Si el número de resultados no coincide
        Exception: Si hay error en la llamada a la API
    """
    model = genai.GenerativeModel(
        model_name=get_gemini_model_name(),
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.1,
        }
    )
    
    response = model.generate_content(prompt, request_options={"timeout": timeout})
    batch_results = json.loads(response.text.strip())
    
    if len(batch_results) != expected_size:
        raise ValueError(f"Se esperaban {expected_size} resultados pero se recibieron {len(batch_results)}")
    
    return batch_results


def parse_json_response(json_text: str) -> Dict[str, Any]:
    """
    Parsea la respuesta JSON de Gemini con limpieza automática.
    
    Args:
        json_text: Texto JSON de la respuesta
        
    Returns:
        Dict parseado
        
    Raises:
        json.JSONDecodeError: Si el JSON es inválido después de limpieza
        ValueError: Si la respuesta es una lista en lugar de un diccionario
    """
    json_text = json_text.strip()
    
    try:
        result = json.loads(json_text)
    except json.JSONDecodeError:
        json_text = re.sub(r',\s*}', '}', json_text)
        json_text = re.sub(r',\s*]', ']', json_text)
        result = json.loads(json_text)
    
    if isinstance(result, list):
        if len(result) > 0:
            result = result[0]
        else:
            raise ValueError("La respuesta JSON es una lista vacía")
    
    if not isinstance(result, dict):
        raise ValueError(f"Se esperaba un diccionario pero se recibió: {type(result)}")
    
    return result
