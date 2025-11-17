"""
Componente de carga inicial de datos (pantalla principal cuando no hay datos).
"""

import streamlit as st
import pandas as pd

from src.data.validation import get_validation_summary
from src.core.database import save_processed_data
from .csv_handler import (
    validate_and_normalize_file,
    categorize_dataframe,
    display_file_summary
)


def render_initial_uploader() -> None:
    """
    Renderiza la pantalla de carga inicial cuando no hay datos.
    Esta es la entrada principal de datos al sistema.
    """
    st.title("📊 Vambe Analytics Dashboard")
    st.markdown("---")
    
    st.info("""
    👋 **¡Bienvenido!** 
    
    Para comenzar, carga un archivo CSV o Excel con los datos de tus clientes.
    El sistema categorizará automáticamente las transcripciones usando IA.
    """)
    
    st.markdown("")
    
    with st.expander("📋 Estructura requerida del archivo", expanded=True):
        st.markdown("""
        Tu archivo debe contener las siguientes columnas:
        
        | Columna | Descripción | Ejemplo |
        |---------|-------------|---------|
        | **Nombre** | Nombre del cliente | Juan Pérez |
        | **Correo Electronico** | Email del cliente | juan@empresa.com |
        | **Numero de Telefono** | Teléfono | +1234567890 |
        | **Fecha de la Reunion** | Fecha de reunión | 2024-01-15 o 15/01/2024 |
        | **Vendedor asignado** | Vendedor responsable | María García |
        | **closed** | Estado (cerrado/abierto) | 1/0 |
        | **Transcripcion** | Texto de la transcripción | "Durante nuestra conversacion, comente que..." |
        
        ⚠️ **Importante**: La columna `Transcripcion` es obligatoria y no puede estar vacía.
        """)
    
    st.markdown("---")
    
    st.subheader("📤 Selecciona tu archivo")
    
    uploaded_file = st.file_uploader(
        "Arrastra y suelta tu archivo aquí, o haz clic para seleccionarlo",
        type=["csv", "xlsx", "xls"],
        help="Formatos soportados: CSV, Excel (.xlsx, .xls)"
    )
    
    if uploaded_file is not None:
        try:
            df_normalized = validate_and_normalize_file(uploaded_file)
            
            if df_normalized is None:
                st.info("💡 **Consejo**: Revisa la estructura requerida arriba y asegúrate de que tu archivo tenga todas las columnas.")
                return
            
            summary = get_validation_summary(df_normalized)
            display_file_summary(summary, df_normalized, compact=False)
            
            st.markdown("---")
            
            if "processing_complete" not in st.session_state:
                st.session_state.processing_complete = False
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                button_pressed = st.button(
                    "🚀 Iniciar Categorización con IA",
                    type="primary",
                    use_container_width=True,
                    disabled=st.session_state.processing_complete,
                    help="Esto procesará todas las transcripciones con Google Gemini AI"
                )
                
                if button_pressed:
                    _process_and_save_initial_data(df_normalized)
                    
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            st.exception(e)


def _process_and_save_initial_data(df: pd.DataFrame) -> None:
    """
    Procesa los datos iniciales (categorización con IA) y los guarda en la base de datos.
    
    Args:
        df: DataFrame normalizado con los datos iniciales
    """
    try:
        total_rows = len(df)
        
        df_categorized = categorize_dataframe(df, show_progress=True)
        
        status_container = st.empty()
        status_container.info("💾 Guardando datos en la base de datos...")
        save_processed_data(df_categorized)
        status_container.empty()
        
        st.session_state.processing_complete = True
        
        st.success(f"✅ ¡Proceso completado exitosamente!")
        
        st.markdown("---")
        
        st.info(f"""
        **📊 Resumen del procesamiento:**
        - ✅ {total_rows} registros categorizados con IA
        - 💾 Datos guardados en la base de datos
        - 🚀 Dashboard listo para usar
        """)
        
        st.markdown("")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎉 Ver Dashboard", type="primary", use_container_width=True):
                st.rerun()
            
    except Exception as e:
        st.error(f"❌ Error durante el procesamiento: {str(e)}")
        st.exception(e)
