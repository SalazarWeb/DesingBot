#!/bin/bash

# Script para configurar el webhook de Telegram para Vercel
# Uso: ./setup_webhook.sh https://tu-bot.vercel.app

if [ -z "$1" ]; then
    echo "❌ Error: Debes proporcionar la URL de tu aplicación en Vercel"
    echo ""
    echo "Uso: ./setup_webhook.sh https://tu-bot.vercel.app"
    echo ""
    echo "Pasos:"
    echo "1. Despliega tu bot en Vercel"
    echo "2. Copia la URL que te da Vercel"
    echo "3. Ejecuta: ./setup_webhook.sh https://tu-url.vercel.app"
    exit 1
fi

VERCEL_URL="$1"
WEBHOOK_URL="${VERCEL_URL}/webhook"

# Cargar TOKEN desde .env si existe
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

if [ -z "$TOKEN" ]; then
    echo "❌ Error: TOKEN no encontrado"
    echo "Por favor:"
    echo "1. Crea un archivo .env con: TOKEN=tu_token_de_botfather"
    echo "2. O ejecuta: export TOKEN=tu_token_de_botfather"
    exit 1
fi

echo "🔗 Configurando webhook para DesignBot..."
echo "📡 URL del webhook: $WEBHOOK_URL"
echo ""

# Configurar webhook
response=$(curl -s -X POST "https://api.telegram.org/bot$TOKEN/setWebhook" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"$WEBHOOK_URL\"}")

# Verificar respuesta
if echo "$response" | grep -q '"ok":true'; then
    echo "✅ ¡Webhook configurado exitosamente!"
    echo ""
    echo "📊 Información del webhook:"
    curl -s "https://api.telegram.org/bot$TOKEN/getWebhookInfo" | \
        python3 -m json.tool
    echo ""
    echo "🎉 ¡Tu bot ya está funcionando en Vercel!"
    echo "🔗 URL de salud: ${VERCEL_URL}/health"
else
    echo "❌ Error configurando webhook:"
    echo "$response" | python3 -m json.tool
    exit 1
fi

echo ""
echo "🚀 ¡Bot desplegado exitosamente!"
echo ""
echo "URLs importantes:"
echo "- Bot: https://t.me/$(curl -s "https://api.telegram.org/bot$TOKEN/getMe" | grep -o '"username":"[^"]*"' | cut -d'"' -f4)"
echo "- Webhook: $WEBHOOK_URL"
echo "- Health: ${VERCEL_URL}/health"
echo "- Dashboard: $VERCEL_URL"