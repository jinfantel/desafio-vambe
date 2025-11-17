"""
Utilidades generales para el dashboard Vambe Analytics.
Este módulo re-exporta todas las funciones desde submódulos especializados.
"""

from .formatting import (
    format_percentage,
    format_number,
    clean_transcript_for_display
)

from .scoring import calculate_lead_score

from .filters import filter_dataframe

from .helpers import (
    get_color_by_value,
    get_month_name_es
)

from .data_parsing import (
    parse_json_field,
    build_preocupaciones_texto
)

__all__ = [
    "format_percentage",
    "format_number",
    "clean_transcript_for_display",
    
    "calculate_lead_score",
    
    "filter_dataframe",
    
    "get_color_by_value",
    "get_month_name_es",
    
    "parse_json_field",
    "build_preocupaciones_texto"
]
