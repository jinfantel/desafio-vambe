"""
Configuración de Gemini AI.
"""

import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"


def configure_gemini() -> None:
    """
    Configura la API de Google Gemini.
    Debe ser llamada antes de usar el categorizador.
    
    Raises:
        SystemExit: Si GEMINI_API_KEY no está configurada
    """
    if not GEMINI_API_KEY:
        st.error("⚠️ GEMINI_API_KEY no está configurada. Por favor, configura la variable de entorno.")
        st.stop()
    
    genai.configure(api_key=GEMINI_API_KEY)


def get_gemini_model_name() -> str:
    """Retorna el nombre del modelo de Gemini configurado."""
    return GEMINI_MODEL
