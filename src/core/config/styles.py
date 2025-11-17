"""
Estilos CSS personalizados para la interfaz de Streamlit.
"""

CUSTOM_CSS = """
<style>
    /* Ajustes generales */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Métricas grandes y destacadas */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    /* Sidebar styling - adaptable a dark/light mode */
    [data-testid="stSidebar"] {
        padding: 2rem 1rem;
    }
    
    /* NO forzar colores de fondo ni texto - dejar que Streamlit los maneje */
    
    /* Botones personalizados */
    .stButton>button {
        background-color: #1E3A8A;
        color: white !important;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #3B82F6;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.4);
    }
    
    /* Tabs styling - adaptable a dark mode */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: white !important;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Títulos de sección - sin forzar colores */
    h1 {
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 600;
    }
    
    /* Forzar sidebar siempre desplegada y ocultar menús superiores no deseados */
    /* 1) Forzar que la sidebar esté visible y quede en su lugar incluso si el usuario intenta colapsarla */
    section[data-testid="stSidebar"] {
        position: relative !important;
        transform: none !important;
        left: 0 !important;
        margin-left: 0 !important;
        width: 300px !important;
        min-width: 260px !important;
        display: block !important;
        visibility: visible !important;
    }

    /* 2) Ocultar botones de colapsar/expandir de la interfaz (evita que se oculte la sidebar)
       Usamos varios selectores por compatibilidad entre versiones */
    button[aria-label*="Toggle sidebar"],
    button[aria-label*="Collapse"],
    button[aria-label*="Expand"],
    button[aria-label*="Open navigation"],
    button[aria-label*="Close navigation"] {
        display: none !important;
    }
    
    /* Ocultar específicamente el botón dentro de la sidebar que la achica */
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebar"] button[kind="headerNoPadding"],
    section[data-testid="stSidebar"] > div > button {
        display: none !important;
    }

    /* 3) Ocultar menú superior (Deploy / Print / Record) dejando el resto de la cabecera intacta */
    #MainMenu {
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
    }

    /* También ocultar toolbar si existe */
    div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* 4) Ocultar elementos de la pantalla de carga (splash screen) */
    /* Ocultar TODOS los iconos y botones del header superior derecho */
    header[data-testid="stHeader"],
    .stApp > header,
    div[data-testid="stStatusWidget"],
    div[data-testid="stDecoration"],
    button[data-testid="baseButton-header"],
    button[data-testid="baseButton-headerNoPadding"],
    button[kind="header"],
    button[kind="headerNoPadding"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
        pointer-events: none !important;
    }
    
    /* Ocultar específicamente los 3 iconos de la esquina superior derecha */
    header svg,
    header button,
    header img,
    [data-testid="stHeader"] svg,
    [data-testid="stHeader"] button,
    [data-testid="stHeader"] img {
        display: none !important;
    }
    
    /* Forzar que NO aparezca nada en la zona superior */
    .stApp {
        padding-top: 0 !important;
    }
</style>
"""
