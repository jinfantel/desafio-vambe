"""
Funciones de cálculo de scoring y métricas de leads.
"""

from typing import List

from src.core.config import VOLUMEN_SCORE_MAP, URGENCIA_SCORE_MAP


def calculate_lead_score(
    volumen_nivel: str,
    urgencia: str,
    es_pico_estacional: bool,
    potencial_upsell: List[str],
    volumen_numerico: int = None,
    fuente_primaria: str = "",
    fuente_detalle: str = "",
    sector_principal: str = "",
    transcript: str = ""
) -> float:
    """
    Calcula el Índice de Potencial de Lead (0-100).
    
    Fórmula original mejorada:
    score = (volumen_score + urgencia_score + escalabilidad_score) / 3 + bonus
    
    Bonus adicionales:
    - Trigger externo (recomendación, evento): +5 pts
    - Presupuesto implícito (sector/internacional): +5 pts
    
    Args:
        volumen_nivel: Nivel de volumen del lead
        urgencia: Nivel de urgencia
        es_pico_estacional: Si tiene picos estacionales
        potencial_upsell: Lista de add-ons potenciales
        volumen_numerico: Número exacto de interacciones (opcional)
        fuente_primaria: Fuente de descubrimiento
        fuente_detalle: Detalle de la fuente
        sector_principal: Sector del lead
        transcript: Transcripción completa
        
    Returns:
        Score entre 0 y 100
    """
    volumen_score = VOLUMEN_SCORE_MAP.get(volumen_nivel, 0)
    
    urgencia_score = URGENCIA_SCORE_MAP.get(urgencia, 30)
    
    escalabilidad_score = 40
    
    if es_pico_estacional:
        escalabilidad_score = 100
    elif "Multilingüe" in potencial_upsell or "Internacional" in str(potencial_upsell):
        escalabilidad_score = 100
    elif len(potencial_upsell) >= 3:
        escalabilidad_score = 70
    
    base_score = (volumen_score + urgencia_score + escalabilidad_score) / 3
    
    trigger_bonus = _calculate_trigger_bonus(fuente_primaria, fuente_detalle, transcript)
    
    budget_bonus = _calculate_budget_bonus(sector_principal, transcript)
    
    final_score = base_score + trigger_bonus + budget_bonus
    
    return round(min(100.0, final_score), 1)


def _calculate_trigger_bonus(fuente_primaria: str, fuente_detalle: str, transcript: str) -> float:
    """
    Bonus por trigger externo (referencia confiable).
    
    +5 pts: Recomendación, conferencia, webinar, evento, LinkedIn
    +3 pts: Búsqueda activa (Google, artículo)
    +0 pts: Sin fuente clara
    """
    combined_text = f"{fuente_primaria} {fuente_detalle} {transcript}".lower()
    
    high_quality_triggers = [
        "recomendación", "recomendó", "colega", "amigo en la industria",
        "conferencia", "seminario", "webinar", "feria", "evento",
        "linkedin", "podcast", "charla", "taller", "forum"
    ]
    
    active_search = ["google", "artículo", "búsqueda", "encontré"]
    
    if any(trigger in combined_text for trigger in high_quality_triggers):
        return 5.0
    elif any(search in combined_text for search in active_search):
        return 3.0
    
    return 0.0


def _calculate_budget_bonus(sector_principal: str, transcript: str) -> float:
    """
    Bonus por presupuesto implícito (capacidad de pago).
    
    +5 pts: Sectores con alto presupuesto o indicadores internacionales
    +3 pts: Sectores medios (salud, educación, retail grande)
    +0 pts: Sectores pequeños o sin info
    """
    transcript_lower = transcript.lower()
    
    budget_indicators = [
        "internacional", "global", "multinacional", "múltiples sedes",
        "operaciones internacionales", "distintos países",
        "gran escala", "corporativo", "empresa grande"
    ]
    
    high_budget_sectors = [
        "Tecnología / Software / SaaS",
        "Consultoría",
        "Salud"
    ]
    
    if any(indicator in transcript_lower for indicator in budget_indicators):
        return 5.0
    
    if sector_principal in high_budget_sectors:
        return 3.0
    
    return 0.0
