#!/bin/bash

# Script de inicio rápido para Vambe Analytics Dashboard

echo "🚀 Iniciando Vambe Analytics Dashboard..."
echo ""

# Verificar si .env existe
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado."
    echo "📝 Creando .env desde .env.example..."
    cp .env.example .env
    echo ""
    echo "❗ IMPORTANTE: Edita el archivo .env y configura tu GEMINI_API_KEY"
    echo "   Obtén tu key en: https://aistudio.google.com/app/apikey"
    echo ""
    read -p "Presiona Enter cuando hayas configurado tu API key..."
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Ejecutar Streamlit
echo "📊 Abriendo dashboard..."
echo ""
./venv/bin/python -m streamlit run app.py
