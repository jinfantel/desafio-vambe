"""
JSON Schema para structured output de Google Gemini.
Define la estructura de categorización de transcripciones.
"""

from typing import Dict, Any

CATEGORIZATION_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "sector_principal": {
            "type": "string",
            "enum": [
                "Tecnología / Software / SaaS",
                "Retail / E-commerce",
                "Salud",
                "Consultoría",
                "Educación / EdTech",
                "Alimentación / Restaurantes / Catering",
                "Logística / Transporte",
                "Turismo / Hospitalidad",
                "Eventos",
                "Moda sostenible",
                "Otros"
            ],
            "description": "Sector principal de la empresa según la transcripción. Usa exactamente uno de estos valores."
        },
        "sector_secundario": {
            "type": ["string", "null"],
            "description": "Subsector específico (ej: EdTech, Fintech, SaaS, Clínica, etc.)"
        },
        "volumen_numerico": {
            "type": ["integer", "null"],
            "description": "Número concreto de interacciones mencionado"
        },
        "volumen_nivel": {
            "type": "string",
            "enum": ["Bajo (<100)", "Medio (100-250)", "Alto (251-500)", "Muy Alto (>500)", "Desconocido"]
        },
        "es_pico_estacional": {
            "type": "boolean",
            "description": "True si menciona picos, temporada alta, promociones, duplicarse/triplicarse"
        },
        "fuente_primaria": {
            "type": "string",
            "enum": [
                "Evento/Conferencia",
                "Recomendación",
                "Búsqueda Online",
                "LinkedIn/Publicación",
                "Webinar/Podcast",
                "Otro"
            ]
        },
        "fuente_detalle": {
            "type": "string",
            "description": "Detalle específico de la fuente (ej: Conferencia Fintech, Google, etc.)"
        },
        "preocupaciones": {
            "type": "array",
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "tipo": {
                        "type": "string",
                        "enum": [
                            "Integración con sistemas",
                            "Personalización/Tono de marca",
                            "Confidencialidad/Compliance",
                            "Multilingüe/Internacional",
                            "Volumen extremo",
                            "Consultas técnicas complejas",
                            "Urgencia en tiempo real",
                            "Otra"
                        ]
                    },
                    "impacto": {
                        "type": "string",
                        "enum": ["Alto", "Medio", "Bajo"]
                    },
                    "ejemplo_frase": {
                        "type": "string",
                        "description": "Copia textual breve de la transcripción"
                    }
                },
                "required": ["tipo", "impacto", "ejemplo_frase"]
            }
        },
        "urgencia_nivel": {
            "type": "string",
            "enum": ["Alta", "Media", "Baja"],
            "description": "Alta = picos, saturación, insostenible, duplicarse"
        },
        "potencial_upsell": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "Multilingüe",
                    "Integración CRM/Tickets",
                    "Respuestas en tiempo real",
                    "Personalización avanzada",
                    "Compliance salud",
                    "Programación automática"
                ]
            }
        }
    },
    "required": [
        "sector_principal",
        "sector_secundario",
        "volumen_numerico",
        "volumen_nivel",
        "es_pico_estacional",
        "fuente_primaria",
        "fuente_detalle",
        "preocupaciones",
        "urgencia_nivel",
        "potencial_upsell"
    ]
}
