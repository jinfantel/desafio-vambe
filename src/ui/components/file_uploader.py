"""
Componente de carga de archivos para agregar datos incrementalmente.
"""

import streamlit as st
import pandas as pd

from src.data.validation import get_validation_summary
from src.core.database import append_processed_data, check_duplicates
from .csv_handler import (
    validate_and_normalize_file,
    categorize_dataframe,
    display_file_summary
)


def render_file_uploader() -> None:
    """
    Renderiza el componente de carga de archivos.
    Permite subir CSV/Excel y agregar datos a la base de datos existente.
    """
    st.subheader("📤 Cargar Datos Adicionales")
    
    st.markdown("""
    Sube un archivo CSV o Excel con nuevos clientes para agregar a la base de datos.
    El archivo debe tener las siguientes columnas:
    - **Nombre**: Nombre del cliente
    - **Correo Electronico**: Email del cliente
    - **Numero de Telefono**: Teléfono del cliente
    - **Fecha de la Reunion**: Fecha de la reunión (formato: YYYY-MM-DD o DD/MM/YYYY)
    - **Vendedor asignado**: Vendedor responsable
    - **closed**: Estado (1/0)
    - **Transcripcion**: Texto de la transcripción (requerido para categorización)
    """)
    
    uploaded_file = st.file_uploader(
        "Selecciona un archivo",
        type=["csv", "xlsx", "xls"],
        help="Archivos CSV o Excel (.xlsx, .xls)"
    )
    
    if uploaded_file is not None:
        try:
            df_normalized = validate_and_normalize_file(uploaded_file)
            
            if df_normalized is None:
                return
            
            summary = get_validation_summary(df_normalized)
            display_file_summary(summary, df_normalized, compact=True)
            
            if st.button("✅ Procesar y Agregar Datos", type="primary", use_container_width=True):
                _process_and_append_data(df_normalized)
                
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")


def _process_and_append_data(df: pd.DataFrame) -> None:
    """
    Procesa los datos (categorización con IA) y los agrega a la base de datos.
    
    Args:
        df: DataFrame normalizado con los nuevos datos
    """
    try:
        df_filtrado, duplicados = check_duplicates(df)
        
        if duplicados > 0:
            st.warning(f"⚠️ Se encontraron {duplicados} registros duplicados que serán omitidos. Solo se procesarán {len(df_filtrado)} registros nuevos.")
        
        if len(df_filtrado) == 0:
            st.info("ℹ️ Todos los registros del archivo ya están en la base de datos. No se realizará ningún procesamiento.")
            if st.button("🔙 Volver", type="secondary", use_container_width=True, key="back_after_all_duplicates"):
                st.rerun()
            return
        
        df_categorized = categorize_dataframe(df_filtrado, show_progress=True)
        
        status_container = st.empty()
        status_container.info("💾 Guardando datos en la base de datos...")
        rows_added = append_processed_data(df_categorized)
        status_container.empty()
        
        additional_duplicates = len(df_categorized) - rows_added
        total_duplicates = duplicados + additional_duplicates
        
        if rows_added > 0:
            st.success(f"✅ ¡Proceso completado! Se agregaron {rows_added} nuevos registros.")
        
        if total_duplicates > 0:
            st.warning(f"⚠️ Se omitieron {total_duplicates} registros duplicados en total (ya existían en la base de datos)")
        
        st.markdown("---")
        
        if rows_added > 0:
            if st.button("🔄 Recargar Dashboard", type="primary", use_container_width=True, key="reload_after_upload"):
                st.rerun()
        else:
            if st.button("🔙 Volver", type="secondary", use_container_width=True, key="back_after_no_upload"):
                st.rerun()
            
    except Exception as e:
        st.error(f"❌ Error durante el procesamiento: {str(e)}")
        st.exception(e)
