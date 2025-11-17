"""
🚀 VAMBE ANALYTICS DASHBOARD
Panel de métricas de ventas para el equipo comercial de Vambe.

Analiza transcripciones de reuniones con clientes usando Google Gemini AI
y genera insights accionables para maximizar conversiones.

Arquitectura modular con src/:
- src/ui/: Interfaz y componentes
- src/data/: Carga y procesamiento
- src/analytics/: Métricas de negocio
- src/core/database/: Persistencia SQLite
- src/core/ai/: Integración Gemini AI
- src/core/config/: Configuración
- src/core/utils/: Utilidades
"""

import streamlit as st

from src.core.config import CUSTOM_CSS
from src.data import load_or_process_data
from src.ui import render_sidebar, apply_filters
from src.ui import render_overview_tab, render_deep_analysis_tab, render_hot_leads_tab, render_concerns_tab
from src.ui.components import render_initial_uploader


def configure_page() -> None:
    """Configura la página de Streamlit con estilos y layout."""
    st.set_page_config(
        page_title="Vambe Analytics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items=None
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_header() -> None:
    """Renderiza el encabezado principal de la aplicación."""
    st.title("📊 Vambe Analytics Dashboard")
    st.markdown(
        "**Panel de Métricas de Ventas** · Powered by Google Gemini AI",
        unsafe_allow_html=True
    )
    st.markdown("---")


def validate_filtered_data(df_filtered) -> bool:
    """
    Valida que hay datos después de aplicar filtros.
    
    Args:
        df_filtered: DataFrame filtrado
        
    Returns:
        True si hay datos, False si no
    """
    if len(df_filtered) == 0:
        st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados.")
        return False
    return True


def render_tabs(df_filtered) -> None:
    """
    Renderiza las pestañas principales del dashboard.
    
    Args:
        df_filtered: DataFrame filtrado con los datos
    """
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Overview",
        "🔬 Análisis Profundo",
        "🔥 Hot Leads",
        "⚠️ Preocupaciones"
    ])
    
    with tab1:
        render_overview_tab(df_filtered)
    
    with tab2:
        render_deep_analysis_tab(df_filtered)
    
    with tab3:
        render_hot_leads_tab(df_filtered)
    
    with tab4:
        render_concerns_tab(df_filtered)


def main() -> None:
    """
    Función principal de la aplicación.
    
    Flujo:
    1. Configurar página
    2. Intentar cargar datos desde SQLite
    3. Si no hay datos: mostrar pantalla de carga inicial
    4. Si hay datos: mostrar dashboard con filtros y métricas
    """
    configure_page()
    
    df = load_or_process_data()
    
    if df is None:
        render_initial_uploader()
        return
    
    render_header()
    
    filters = render_sidebar(df)
    
    df_filtered = apply_filters(df, filters)
    
    if not validate_filtered_data(df_filtered):
        st.stop()
    
    render_tabs(df_filtered)


if __name__ == "__main__":
    main()
