# 🚀 Vambe Analytics Dashboard

> **Panel de Análisis de Ventas** powered by Google Gemini AI

Dashboard que transforma transcripciones de reuniones con clientes en insights accionables usando Inteligencia Artificial.

---

## 🎯 ¿Qué hace?

Usa **Google Gemini AI** para:
1. Categorizar automáticamente cada transcripción en 10 dimensiones
2. Calcular un Índice de Potencial (0-100) por lead
3. Identificar patrones y visualizar insights

### Resultado
**Decisiones basadas en datos**, no en intuición.

---

## 📊 Métricas Principales

### 1. Índice de Potencial de Lead (0-100) ⭐
Score automático basado en volumen, urgencia y escalabilidad.
- **80-100**: 🔥 Prioridad ALTA
- **60-79**: ⚡ Prioridad MEDIA  
- **40-59**: 📝 Prioridad BAJA
- **<40**: ❄️ Descalificar

### 2. Tasa de Cierre
- Global + Pronóstico 6 meses
- Por vendedor (con benchmarking)
- Distribución de volumen numérico

### 3. Heatmap Sector × Volumen
Identifica "sweet spots" de conversión (ej: Tecnología + Alto volumen = 90%+ cierre)

### 4. ROI de Fuentes
Compara % leads vs % conversión por canal de descubrimiento

### 5. Top Preocupaciones
Las 5 objeciones más comunes que bloquean cierres

### 6. Upsell Opportunities
Radar de 6 add-ons potenciales según demanda detectada

---

## 🛠️ Instalación

### Requisitos
- Python 3.9+
- Cuenta de Google (para API key gratuita)

### Pasos

1. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar API Key**
```bash
cp .env.example .env
nano .env  # Pega GEMINI_API_KEY
```

4. **Ejecutar**
```bash
streamlit run app.py
# O simplemente: ./run.sh
```

---

## 💾 Cómo Funciona

### Primera Vez
1. Es necesario subir un archivo CSV/Excel con las columnas requeridas
2. El sistema valida el formato automáticamente
3. Gemini categoriza cada transcripción
4. Resultados se guardan en SQLite local

### Siguientes Veces
- Carga instantánea desde la base de datos (< 1 seg)
- Se pueden subir más datos desde la barra lateral
- Los nuevos datos se agregan y categorizan automáticamente

### Columnas Requeridas en CSV
- `Nombre` - Nombre del cliente/empresa
- `Correo Electronico` - Email de contacto
- `Numero de Telefono` - Teléfono
- `Fecha de la Reunion` - Fecha (formato: DD/MM/YYYY)
- `Vendedor asignado` - Nombre del vendedor
- `closed` - Estado (0 = abierto, 1 = cerrado)
- `Transcripcion` - Texto completo de la reunión

---

## 🏗️ Arquitectura

### Estructura del Proyecto
```
vambe-analytics/
├── app.py                      # Aplicación principal
├── src/
│   ├── core/
│   │   ├── ai/                 # Integración Gemini AI
│   │   ├── config/             # Configuración (API, schemas, colores)
│   │   ├── database/           # SQLite (modularizado: crud, duplicates, serialization)
│   │   └── utils/              # Helpers (scoring, formatting, filters)
│   ├── analytics/              # 8 métricas (close_rate, roi, leads, etc)
│   ├── data/                   # Validación, carga, API de datos
│   └── ui/
│       ├── components/         # Modularizado: file_reader, ai_processor, etc
│       ├── tabs/               # 4 tabs principales
│       └── sidebar.py          # Barra lateral con filtros
├── data_files/
│   └── vambe_processed.db      # SQLite database (auto-generada)
├── requirements.txt
├── .env.example
└── README.md
```

### Flujo de Datos
```
CSV/Excel Upload
    ↓
Validación de schema
    ↓
Gemini AI (batch de 5)
    ↓
10 dimensiones extraídas
    ↓
SQLite persistence
    ↓
Filtros + Métricas
    ↓
Visualizaciones Plotly
```

### Dimensiones Extraídas (10)
1. **sector_principal** - Industria principal
2. **sector_secundario** - Sub-categoría
3. **volumen_numerico** - Número exacto mencionado
4. **volumen_nivel** - Bajo/Medio/Alto/Muy Alto
5. **es_pico_estacional** - Boolean (picos o estable)
6. **fuente_primaria** - Canal de descubrimiento
7. **fuente_detalle** - Contexto específico
8. **preocupaciones** - Array de objeciones (max 3)
9. **urgencia_nivel** - Baja/Media/Alta
10. **potencial_upsell** - Array de add-ons potenciales

---

## 🧠 Decisiones Clave de Diseño

### 1. Arquitectura Modular
**Decisión:** Separar el código en módulos independientes (`core`, `analytics`, `data`, `ui`)

**Justificación:**
- ✅ **Mantenibilidad:** Cada módulo tiene una responsabilidad única
- ✅ **Escalabilidad:** Fácil agregar nuevas métricas sin afectar el resto
- ✅ **Testing:** Permite probar componentes de forma aislada

### 2. Procesamiento en Batch de 5
**Decisión:** Enviar 5 transcripciones juntas por llamada API

**Justificación:**
- ✅ **Costo:** Procesar 1 transcripción = 1 llamada. Con batch: 5 transcripciones = 1 llamada (5x más eficiente)
- ✅ **Tiempo:** Batch de 1 es muy lento (~10 min para 60 clientes). Batch de 5 reduce a ~3 min
- ✅ **Confiabilidad:** Batches muy grandes generan respuestas JSON incompletas o truncadas
- ✅ **Rate limits:** Optimiza el uso de los límites de la API gratuita

### 3. SQLite como Base de Datos
**Decisión:** SQLite local en lugar de PostgreSQL/MySQL

**Justificación:**
- ✅ **Zero-config:** No requiere servidor de BD
- ✅ **Portabilidad:** Un solo archivo `.db`
- ✅ **Suficiente:** Óptimo para <10K registros

### 4. Stack Python: Pandas + Plotly + Streamlit
**Decisión:** Ecosistema Python completo para análisis de datos

**Justificación:**
- ✅ **Python:** Lenguaje nativo para Data Science y ML
- ✅ **Pandas:** Manipulación de datos tabular (filtros, agregaciones, transformaciones)
- ✅ **Plotly:** Gráficos interactivos
- ✅ **Velocidad de desarrollo:** Dashboard funcional en 3-5 días
- ✅ **Python puro:** No requiere JavaScript
- ✅ **Reactivo nativo:** Filtros actualizan métricas automáticamente
- ✅ **Ideal para MVPs**

**Trade-off:** Limitado a ~1000 usuarios concurrentes (suficiente para este caso)

### 6. Sistema de Scoring de Leads
**Decisión:** Fórmula cuantitativa basada en 3 pilares + bonuses

**Justificación:**
```python
base_score = (volumen_score + urgencia_score + escalabilidad_score) / 3
final_score = base_score + trigger_bonus + budget_bonus

Donde:
- volumen_score: 0-100 según nivel de volumen semanal
  · Desconocido: 0 pts
  · Bajo (<100): 20 pts
  · Medio (100-250): 50 pts
  · Alto (251-500): 80 pts
  · Muy Alto (>500): 100 pts

- urgencia_score: 0-100 según nivel de urgencia
  · Baja: 30 pts
  · Media: 60 pts
  · Alta: 100 pts

- escalabilidad_score: 0-100 según potencial de crecimiento
  · Picos estacionales: 100 pts
  · Soporte multicanal: 100 pts
  · Escalamiento automático: 90 pts
  · 3+ add-ons: 70 pts
  · Base: 40 pts

- trigger_bonus: +0 a +5 pts
  · Recomendación/Evento/LinkedIn: +5 pts
  · Búsqueda activa (Google): +3 pts
  · Sin fuente clara: 0 pts

- budget_bonus: +0 a +5 pts
  · Indicadores internacionales: +5 pts
  · Sectores de alto presupuesto: +3 pts
  · Sin info: 0 pts
```

**Ventaja:** Priorización objetiva y replicable de leads.

### 7. Retry con Exponential Backoff
**Decisión:** Reintentar 3 veces con delays incrementales (1s, 2s, 4s)

**Justificación:**
- ✅ **Resilencia:** Maneja fallos temporales de API
- ✅ **Graceful degradation:** Usa valores por defecto si falla definitivamente
- ✅ **No bloquea:** El usuario ve progreso incluso con errores parciales

### 8. Normalización de Volumen
**Decisión:** Convertir todo a "interacciones por semana"

**Justificación:**
```
Problema: Clientes mencionan "80 diarias", "500 semanales", "2000 mensuales"
Solución: Normalizar en el prompt de Gemini
  - Diarias → × 7
  - Semanales → sin cambio
  - Mensuales → ÷ 4
```

**Ventaja:** Permite comparar clientes de forma consistente.
