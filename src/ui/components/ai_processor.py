"""
Procesamiento de archivos con IA (Google Gemini).
"""

import streamlit as st
import pandas as pd

from src.data.transformer import expand_categories_to_dataframe
from src.core.ai import batch_categorize_transcripts, configure_gemini


def categorize_dataframe(df: pd.DataFrame, show_progress: bool = True) -> pd.DataFrame:
    """
    Categoriza todas las transcripciones de un DataFrame usando Gemini AI en batches.
    
    Args:
        df: DataFrame con los datos normalizados
        show_progress: Si debe mostrar la barra de progreso
        
    Returns:
        DataFrame con categorías expandidas
    """
    configure_gemini()
    
    total_rows = len(df)
    
    if show_progress:
        progress_bar = st.progress(0, text="Iniciando categorización con IA...")
        status_container = st.empty()
        status_container.info(f"🤖 Categorizando {total_rows} transcripciones con Google Gemini AI...")
    
    def update_progress(current, total):
        if show_progress:
            progress = current / total
            progress_bar.progress(
                progress,
                text=f"Procesando {current} de {total} transcripciones"
            )
    
    categories = batch_categorize_transcripts(
        transcripts=df["Transcripcion"].tolist(),
        client_names=df["Nombre"].tolist(),
        _progress_callback=update_progress if show_progress else None
    )
    
    df_categorized = expand_categories_to_dataframe(df, categories)
    
    if show_progress:
        progress_bar.empty()
        status_container.empty()
    
    return df_categorized
