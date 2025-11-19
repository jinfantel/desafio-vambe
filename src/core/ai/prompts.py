"""
Construcción de prompts para la categorización con Gemini.
"""

from typing import List


def build_single_categorization_prompt(transcript: str, client_name: str) -> str:
    """
    Construye el prompt para categorización individual.
    
    Args:
        transcript: Texto de la transcripción
        client_name: Nombre del cliente
        
    Returns:
        Prompt formateado para Gemini
    """
    return f"""
Eres un analista experto de ventas B2B. Tu tarea es analizar la siguiente transcripción de una reunión comercial y extraer información estructurada clave.

**Cliente:** {client_name}

**Transcripción:**
{transcript}

{get_categorization_instructions()}

**IMPORTANTE:** Devuelve SOLO el JSON estructurado, sin texto adicional antes o después.
"""


def build_batch_categorization_prompt(
    batch_transcripts: List[str],
    batch_names: List[str],
    batch_start: int,
    batch_size: int
) -> str:
    """
    Construye el prompt para categorización en batch.
    
    Args:
        batch_transcripts: Lista de transcripciones del grupo
        batch_names: Lista de nombres de clientes del grupo
        batch_start: Índice de inicio del grupo
        batch_size: Tamaño del grupo
        
    Returns:
        Prompt formateado para Gemini
    """
    prompt = f"""
        Eres un analista experto de ventas B2B. Analiza las siguientes {batch_size} transcripciones de reuniones comerciales y devuelve un array JSON con exactamente {batch_size} objetos, uno por cada transcripción.

        {get_categorization_instructions()}

        **TRANSCRIPCIONES A ANALIZAR:**

        """
    
    for i, (transcript, name) in enumerate(zip(batch_transcripts, batch_names), 1):
        prompt += f"""
            ---
            **TRANSCRIPCIÓN #{batch_start + i}**
            **Cliente:** {name}
            **Texto:**
            {transcript}

            """
    
    prompt += f"""
        ---

        **IMPORTANTE:** Devuelve SOLO un array JSON con exactamente {batch_size} objetos, sin texto adicional antes o después.
        Formato: [{{"sector_principal": "...", "sector_secundario": "...", ...}}, {{"sector_principal": "...", ...}}, ...]
        """
    
    return prompt


def get_categorization_instructions() -> str:
    """
    Retorna las instrucciones comunes de categorización.
    
    Returns:
        Texto con instrucciones detalladas para el modelo
    """
    return """
        **INSTRUCCIONES CRÍTICAS:**

        1. **sector_principal**: Identifica el sector principal de entre: ["Tecnología / Software / SaaS", "Retail / E-commerce", "Salud", "Consultoría", "Educación / EdTech", "Alimentación / Restaurantes / Catering", "Logística / Transporte", "Turismo / Hospitalidad", "Eventos", "Moda sostenible", "Otros"]. Elige el más cercano o usa "Otros".

        2. **sector_secundario**: Especifica el subsector (ej: "Fintech", "EdTech", "SaaS", "Clínica dental", etc.). Si no hay información, usa null.

        3. **volumen_numerico**: Extrae el número de interacciones mencionadas y NORMALÍZALO A INTERACCIONES POR SEMANA:
        - Si dice "80 diarias" → 80 × 7 = 560 semanales
        - Si dice "500 semanales" → 500 semanales
        - Si dice "2000 mensuales" → 2000 ÷ 4 = 500 semanales
        - Si no hay número concreto, usa null

        4. **volumen_nivel**: Clasifica el volumen SEMANAL:
        - "Bajo (<100)" si < 100 por semana
        - "Medio (100-250)" si 100-250 por semana
        - "Alto (251-500)" si 251-500 por semana
        - "Muy Alto (>500)" si > 500 por semana
        - "Desconocido" si no hay información

        5. **es_pico_estacional**: TRUE si menciona: "picos", "temporada alta", "promociones", "duplicarse", "triplicarse". FALSE en caso contrario.

        6. **fuente_primaria**: De dónde conoció Vambe: ["Evento/Conferencia", "Recomendación", "Búsqueda Online", "LinkedIn/Publicación", "Webinar/Podcast", "Otro"]

        7. **fuente_detalle**: Texto específico que describe la fuente.

        8. **preocupaciones**: Array de MÁXIMO 3 preocupaciones ordenadas por importancia. Para cada una:
        - **tipo**: ["Integración con sistemas", "Personalización/Tono de marca", "Confidencialidad/Compliance", "Multilingüe/Internacional", "Volumen extremo", "Consultas técnicas complejas", "Urgencia en tiempo real", "Otra"]
        - **impacto**: ["Alto", "Medio", "Bajo"]
        - **ejemplo_frase**: Copia textual de 10-30 palabras

        9. **urgencia_nivel**: ["Alta", "Media", "Baja"]

        10. **potencial_upsell**: Array de add-ons valorados: ["Integración con CRM/Tickets existente", "Soporte multicanal (WhatsApp, IG, Email, etc.)", "Escalamiento automático en temporada alta / picos", "Respuestas personalizadas con tono de marca", "Reportes y analíticos de atención al cliente"]
    """
