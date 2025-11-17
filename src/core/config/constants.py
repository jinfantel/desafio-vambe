"""
Constantes y mapeos utilizados en toda la aplicación.
"""

from typing import Dict

VOLUMEN_SCORE_MAP: Dict[str, int] = {
    "Desconocido": 0,
    "Bajo (<100)": 20,
    "Medio (100-250)": 50,
    "Alto (251-500)": 80,
    "Muy Alto (>500)": 100
}

URGENCIA_SCORE_MAP: Dict[str, int] = {
    "Baja": 30,
    "Media": 60,
    "Alta": 100
}
