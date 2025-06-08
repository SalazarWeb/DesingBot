import os
import json
import logging
from flask import Flask, request, jsonify
import sys
sys.path.append('/var/task')
sys.path.append('/var/task/Bot')

# Importar el handler del bot
from Bot.bot_handler import BotHandler
import telebot

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener token desde variables de entorno
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    raise ValueError("TOKEN environment variable is required")

# Inicializar bot
bot = telebot.TeleBot(TOKEN)
bot_handler = BotHandler(bot=bot)

# Crear app Flask
app = Flask(__name__)

def register_webhook_handlers(bot, bot_handler):
    """Registra todos los handlers para webhooks"""
    
    @bot.message_handler(commands=['start'])
    def start(message):
        bot_handler.start(message)

    @bot.message_handler(commands=['design'])
    def design(message):
        bot_handler.handle_general_question(message)

    @bot.message_handler(commands=['ux'])
    def ux(message):
        bot_handler.handle_general_question(message)

    @bot.message_handler(commands=['ui'])
    def ui(message):
        bot_handler.handle_general_question(message)

    @bot.message_handler(commands=['tools'])
    def tools(message):
        bot_handler.handle_general_question(message)

    @bot.message_handler(commands=['ask'])
    def ask(message):
        bot_handler.handle_general_question(message)

    @bot.message_handler(commands=['search'])
    def search(message):
        bot_handler.handle_embedding_search(message)

    @bot.message_handler(commands=['help'])
    def help_command(message):
        bot_handler.show_help(message)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('list_'))
    def callback_list(call):
        bot_handler.handle_list(call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('download#'))
    def callback_download(call):
        bot_handler.handle_pdf_download(call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('back_'))
    def callback_back(call):
        bot_handler.handle_back(call)

    @bot.callback_query_handler(func=lambda call: call.data == 'show_help')
    def callback_show_help(call):
        bot_handler.show_help(call)

    @bot.callback_query_handler(func=lambda call: call.data == 'search_help')
    def callback_search_help(call):
        bot_handler.start(call)

    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def handle_text(message):
        if message.text.startswith('/'):
            bot_handler.show_help(message)
        else:
            bot_handler.handle_message(message)

# Registrar handlers
register_webhook_handlers(bot, bot_handler)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint principal para recibir actualizaciones de Telegram"""
    try:
        # Obtener datos del request
        update = request.get_json()
        
        if update:
            # Procesar actualización
            update_obj = telebot.types.Update.de_json(update)
            bot.process_new_updates([update_obj])
            
            logger.info(f"Webhook procesado exitosamente: {update.get('update_id', 'unknown')}")
            return jsonify({"status": "ok"})
        else:
            logger.warning("Webhook recibido sin datos")
            return jsonify({"status": "no data"}), 400
            
    except Exception as e:
        logger.error(f"Error procesando webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de salud para verificar que el servicio está funcionando"""
    return jsonify({
        "status": "healthy",
        "bot_info": {
            "username": bot.get_me().username if TOKEN else "No token",
            "version": "1.0.0"
        }
    })

@app.route('/', methods=['GET'])
def index():
    """Página principal"""
    return jsonify({
        "message": "🎨 DesignBot API está funcionando!",
        "endpoints": {
            "webhook": "/webhook (POST)",
            "health": "/health (GET)"
        }
    })

# Para deployment en Vercel
def handler(request):
    """Handler principal para Vercel"""
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    # Para testing local
    app.run(debug=True, port=5000)