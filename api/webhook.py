import os
import json
import logging
from flask import Flask, request, jsonify
import sys

# Configurar el path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Bot'))

# Importar el handler del bot
try:
    from Bot.bot_handler import BotHandler
    import telebot
except ImportError as e:
    logging.error(f"Error importando módulos: {e}")
    # Fallback imports
    import telebot

# Configurar logging para Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener token desde variables de entorno
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logger.error("TOKEN environment variable is required")
    raise ValueError("TOKEN environment variable is required")

# Inicializar bot
bot = telebot.TeleBot(TOKEN)

# Inicializar bot_handler solo si la importación fue exitosa
try:
    bot_handler = BotHandler(bot=bot)
    logger.info("BotHandler inicializado correctamente")
except Exception as e:
    logger.error(f"Error inicializando BotHandler: {e}")
    bot_handler = None

# Crear app Flask
app = Flask(__name__)

def register_webhook_handlers(bot, bot_handler):
    """Registra todos los handlers para webhooks"""
    
    @bot.message_handler(commands=['start'])
    def start(message):
        if bot_handler:
            bot_handler.start(message)
        else:
            bot.reply_to(message, "🤖 ¡Hola! Soy DesignBot, tu asistente de UX/UI. El sistema se está inicializando...")

    @bot.message_handler(commands=['help'])
    def help_command(message):
        if bot_handler:
            bot_handler.show_help(message)
        else:
            help_text = """
🎨 *DesignBot - Comandos Disponibles*

/start - Iniciar el bot
/help - Mostrar esta ayuda
/design - Preguntas sobre diseño
/ux - Temas de experiencia de usuario
/ui - Temas de interfaz de usuario
/tools - Herramientas de diseño
/search - Búsqueda en recursos
"""
            bot.reply_to(message, help_text, parse_mode='Markdown')

    @bot.message_handler(commands=['design', 'ux', 'ui', 'tools', 'ask'])
    def handle_design_commands(message):
        if bot_handler:
            bot_handler.handle_general_question(message)
        else:
            bot.reply_to(message, "🔄 El sistema está cargando. Intenta de nuevo en unos segundos.")

    @bot.message_handler(commands=['search'])
    def search(message):
        if bot_handler:
            bot_handler.handle_embedding_search(message)
        else:
            bot.reply_to(message, "🔍 Función de búsqueda temporalmente no disponible.")

    @bot.message_handler(commands=['list'])
    def list_command(message):
        if bot_handler:
            bot_handler.list_categories(message)
        else:
            bot.reply_to(message, "📋 Lista de categorías temporalmente no disponible.")

    # Handlers para callbacks
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query_handler(call):
        if bot_handler:
            bot_handler.handle_callback_query(call)
        else:
            bot.answer_callback_query(call.id, "Sistema inicializándose...")

    # Handler para mensajes de texto
    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def handle_text(message):
        if message.text.startswith('/'):
            help_command(message)
        else:
            if bot_handler:
                bot_handler.handle_general_question(message)
            else:
                bot.reply_to(message, "🤖 Recibí tu mensaje. El sistema se está inicializando, intenta de nuevo en unos segundos.")

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
    try:
        bot_info = bot.get_me()
        return jsonify({
            "status": "healthy",
            "bot_info": {
                "username": bot_info.username,
                "first_name": bot_info.first_name,
                "id": bot_info.id
            },
            "bot_handler_status": "loaded" if bot_handler else "not_loaded",
            "version": "2.0.0"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "bot_handler_status": "loaded" if bot_handler else "not_loaded"
        })

@app.route('/', methods=['GET'])
def index():
    """Página principal"""
    return jsonify({
        "message": "🎨 DesignBot API está funcionando en Vercel!",
        "status": "online",
        "endpoints": {
            "webhook": "/webhook (POST)",
            "health": "/health (GET)"
        },
        "bot_handler": "loaded" if bot_handler else "not_loaded"
    })

# Handler para Vercel (serverless)
def handler(event, context):
    """Handler principal para Vercel serverless"""
    try:
        from werkzeug.wrappers import Request
        from werkzeug.serving import WSGIRequestHandler
        
        # Crear un request wrapper
        request_wrapper = Request(event)
        
        # Procesar con Flask
        response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'body': response.get_data(as_text=True),
            'headers': dict(response.headers)
        }
    except Exception as e:
        logger.error(f"Error en handler de Vercel: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Para testing local
if __name__ == '__main__':
    app.run(debug=True, port=5000)