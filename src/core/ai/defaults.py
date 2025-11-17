"""
Valores por defecto y constantes del categorizador.
"""

from typing import Dict, Any


BATCH_SIZE = 5
RETRY_ATTEMPTS = 3
RATE_LIMIT_DELAY = 2.0
SINGLE_TIMEOUT = 90
BATCH_TIMEOUT = 120
CACHE_TTL = 3600


def get_default_categorization() -> Dict[str, Any]:
    """
    Retorna una categorización por defecto en caso de error.
    
    Returns:
        Dict con valores por defecto para todas las categorías
    """
    return {
        "sector_principal": "Otros",
        "sector_secundario": None,
        "volumen_numerico": None,
        "volumen_nivel": "Desconocido",
        "es_pico_estacional": False,
        "fuente_primaria": "Otro",
        "fuente_detalle": "No disponible",
        "preocupaciones": [],
        "urgencia_nivel": "Media",
        "potencial_upsell": [],
        "_categorization_success": False
    }
