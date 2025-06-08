import os
import logging
import telebot
import time
from telebot import types
from typing import List, Dict, Any, Set, Optional
from ai_embedding.extract import process_documents, search_similar_chunks_sklearn
from ai_embedding.ai import answer_general_question, embed_question
from constants import DOCUMENTS_FOLDER, DESIGN_CATEGORIES


class BotHandler:
    def __init__(self, bot=None):
        """
        Inicializa el manejador del DesignBot UX/UI

        Args:
            bot: Instancia de TeleBot pasada desde main.py
        """
        self._init_logging()
        self.bot = bot
        self.processing_users = set()
        print("🎨 Inicializando DesignBot...")
        self._init_data()

    def _init_logging(self):
        """Configura el logger para esta clase"""
        self.logger = logging.getLogger(__name__)

    def _init_data(self):
        """Inicializa el acceso a los datos procesados"""
        try:
            # Procesamiento de PDFs/vectores realizado solo una vez al inicio
            self.index_model, self.chunks = process_documents()
            if not self.index_model or not self.chunks:
                self.logger.warning("No se pudieron cargar índices o documentos")
        except Exception as e:
            self.logger.error(f"Error inicializando datos: {str(e)}")
            self.index_model = None
            self.chunks = []

    def process_all_pdfs(self):
        """Procesa todos los PDFs para crear embeddings e índices"""
        self.index_model, self.chunks = process_documents()
        return bool(self.index_model and self.chunks)

    def start(self, message_or_call):
        """Maneja el comando start o callback"""
        chat_id = (
            message_or_call.chat.id
            if hasattr(message_or_call, "chat")
            else message_or_call.message.chat.id
        )

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            types.KeyboardButton("🎨 UX Research"),
            types.KeyboardButton("🖼️ UI Patterns"),
        )
        keyboard.add(
            types.KeyboardButton("🎯 Design Systems"), 
            types.KeyboardButton("📱 Case Studies")
        )
        keyboard.add(
            types.KeyboardButton("🔍 Búsqueda"), 
            types.KeyboardButton("❓ Ayuda")
        )
        keyboard.add(
            types.KeyboardButton("🛠️ Herramientas"),
            types.KeyboardButton("♿ Accesibilidad")
        )

        welcome_message = (
            "🎨 **DesignBot - Experto en UX/UI**\n\n"
            "¡Hola! Soy DesignBot, tu asistente especializado en UX/UI Design.\n"
            "Puedo ayudarte con:\n\n"
            "• **`/design`** - Principios y teoría del diseño\n"
            "• **`/ux`** - Research, usabilidad y experiencia de usuario\n"
            "• **`/ui`** - Interfaces, patrones y componentes\n"
            "• **`/tools`** - Guías de Figma, Sketch, Adobe XD\n"
            "• **`/search`** - Buscar en recursos especializados\n\n"
            "💡 También puedes usar `/ask` para consultas generales sobre diseño."
        )

        self.bot.send_message(
            chat_id,
            welcome_message,
            reply_markup=keyboard,
            parse_mode="Markdown",
        )

    def handle_general_question(self, message):
        """Maneja preguntas generales de diseño con la IA"""
        start_time = time.perf_counter()
        
        # Determinar el comando y extraer la pregunta
        text = message.text
        question = ""
        command_type = "general"
        
        if text.startswith("/design "):
            question = text.replace("/design ", "")
            command_type = "design"
        elif text.startswith("/ux "):
            question = text.replace("/ux ", "")
            command_type = "ux"
        elif text.startswith("/ui "):
            question = text.replace("/ui ", "")
            command_type = "ui"
        elif text.startswith("/tools "):
            question = text.replace("/tools ", "")
            command_type = "tools"
        elif text.startswith("/ask "):
            question = text.replace("/ask ", "")
            command_type = "general"
        else:
            question = text.replace("/ask", "").strip()
        
        if not question:
            help_messages = {
                "design": "❌ **Formato correcto:** `/design [tu pregunta sobre diseño]`\n\n📝 *Ejemplo:* `/design principios de diseño visual`",
                "ux": "❌ **Formato correcto:** `/ux [tu pregunta sobre UX]`\n\n📝 *Ejemplo:* `/ux cómo hacer user research efectivo`",
                "ui": "❌ **Formato correcto:** `/ui [tu pregunta sobre UI]`\n\n📝 *Ejemplo:* `/ui mejores prácticas para botones`",
                "tools": "❌ **Formato correcto:** `/tools [tu pregunta sobre herramientas]`\n\n📝 *Ejemplo:* `/tools cómo usar componentes en Figma`",
                "general": "❌ **Formato correcto:** `/ask [tu pregunta]`\n\n📝 *Ejemplo:* `/ask diferencia entre UX y UI`"
            }
            
            self.bot.send_message(
                message.chat.id,
                help_messages.get(command_type, help_messages["general"]),
                parse_mode="Markdown",
            )
            return

        user_id = message.from_user.id
        if user_id in self.processing_users:
            self.bot.send_message(
                message.chat.id,
                "⏳ Ya estoy procesando tu consulta anterior. Por favor espera...",
            )
            return

        self.processing_users.add(user_id)
        
        # Mensaje contextual según el tipo de comando
        context_messages = {
            "design": "🎨 Analizando principios de diseño...",
            "ux": "👥 Consultando mejores prácticas de UX...",
            "ui": "🖼️ Revisando patrones de interfaz...",
            "tools": "🛠️ Buscando guías de herramientas...",
            "general": "💭 Procesando tu consulta de diseño..."
        }
        
        self.bot.send_chat_action(message.chat.id, "typing")
        self.bot.send_message(
            message.chat.id, 
            context_messages.get(command_type, context_messages["general"])
        )

        try:
            # Contextualizar la pregunta según el comando
            if command_type != "general":
                context_prefixes = {
                    "design": "Sobre principios y teoría del diseño: ",
                    "ux": "Sobre experiencia de usuario y research: ",
                    "ui": "Sobre interfaces y patrones UI: ",
                    "tools": "Sobre herramientas de diseño: "
                }
                question = context_prefixes[command_type] + question
            
            self.logger.info(f"Generando respuesta de {command_type} para: {question[:50]}...")
            respuesta = answer_general_question(question)

            safe_response = sanitize_markdown(respuesta)

            if isinstance(safe_response, list):
                for part in safe_response:
                    self.bot.send_message(message.chat.id, part, parse_mode="Markdown")
            else:
                self.bot.send_message(
                    message.chat.id, safe_response, parse_mode="Markdown"
                )

        except Exception as e:
            self.logger.error(f"Error en handle_general_question: {str(e)}")
            self.bot.send_message(
                message.chat.id,
                "❌ No pude generar una respuesta. Por favor, intenta reformular tu pregunta de diseño.",
            )
        finally:
            elapsed = time.perf_counter() - start_time
            self.logger.info(
                f"Tiempo de respuesta de handle_general_question: {elapsed:.3f} segundos"
            )
            self.processing_users.remove(user_id)

    def handle_embedding_search(self, message):
        """Busca documentos relevantes y genera respuesta basada en ellos"""
        start_time = time.perf_counter()
        question = message.text.replace("/search ", "")
        if not question or question == "/search":
            self.bot.send_message(
                message.chat.id, "❌ Formato correcto: /search [tu consulta]"
            )
            return

        user_id = message.from_user.id
        if user_id in self.processing_users:
            self.bot.send_message(
                message.chat.id,
                "⏳ Ya estoy procesando tu consulta anterior. Por favor espera...",
            )
            return

        self.processing_users.add(user_id)
        self.bot.send_chat_action(message.chat.id, "typing")

        try:
            self.logger.info(f"Buscando documentos para: {question[:50]}...")

            # Verificación de datos disponibles
            if not self.index_model or not self.chunks:
                self.bot.send_message(
                    message.chat.id,
                    "⚠️ No hay documentos procesados disponibles para búsqueda.",
                )
                return

            # Generación de embedding para la búsqueda
            question_embedding = embed_question(question)
            if not question_embedding:
                self.bot.send_message(
                    message.chat.id,
                    "❌ No pude procesar tu consulta. Intenta con otra pregunta.",
                )
                return

            # Búsqueda semántica de documentos relevantes
            similar_chunks = search_similar_chunks_sklearn(
                question_embedding, self.index_model, self.chunks, top_k=5
            )

            if not similar_chunks:
                self.bot.send_message(
                    message.chat.id,
                    "❓ No encontré documentos relacionados con tu consulta.",
                )
                return

            # Indicar al usuario que estamos generando la respuesta
            self.bot.send_message(
                message.chat.id,
                "⏳ Generando respuesta basada en los documentos relevantes...",
            )

            # Generar respuesta usando los chunks encontrados
            from ai_embedding.ai import generate_answer

            answer, references = generate_answer(question, similar_chunks, self.chunks)

            # Enviar la respuesta principal (dividida si es necesaria)
            if len(answer) > 4000:  # Cambiado de plain_answer a answer
                chunks = [answer[i : i + 4000] for i in range(0, len(answer), 4000)]
                for chunk in chunks:
                    self.bot.send_message(message.chat.id, chunk)
            else:
                self.bot.send_message(
                    message.chat.id, answer
                )  # Cambiado de plain_answer a answer

            # NUEVA IMPLEMENTACIÓN: Manejo mejorado de referencias
            if similar_chunks:
                # Diccionario para agrupar referencias por documento
                doc_refs = {}  # {documento: set(páginas)}

                # Extraer información única de documentos y páginas
                for chunk in similar_chunks:
                    doc_name = chunk.get("document", "")
                    if not doc_name:
                        continue

                    # Convertir a nombre base del documento
                    base_name = os.path.basename(doc_name)
                    pretty_name = base_name.replace(".pdf", "").replace("_", " ")

                    # Extraer páginas únicas
                    pages = chunk.get("pages", [])

                    # Agregar al diccionario, combinando las páginas si ya existe
                    if pretty_name in doc_refs:
                        doc_refs[pretty_name].update(pages)
                    else:
                        doc_refs[pretty_name] = set(pages)

                # Crear mensaje de referencias
                if doc_refs:
                    ref_text = "📚 Referencias consultadas:\n\n"

                    for doc_name, pages in doc_refs.items():
                        # Ordenar páginas para presentación
                        sorted_pages = sorted(pages)
                        pages_str = (
                            ", ".join(map(str, sorted_pages)) if sorted_pages else "N/A"
                        )
                        ref_text += f"• {doc_name} (Pág: {pages_str})\n"

                    # Enviar mensaje con referencias únicas
                    self.bot.send_message(message.chat.id, ref_text)

                    # Crear botones de descarga (solo uno por documento)
                    keyboard = types.InlineKeyboardMarkup()

                    for doc_pretty_name in doc_refs.keys():
                        # Buscar documento en sistema de archivos
                        found = False
                        for pdf_path in self.find_pdf_files(DOCUMENTS_FOLDER):
                            base_name = os.path.basename(pdf_path)
                            pdf_pretty_name = base_name.replace(".pdf", "").replace(
                                "_", " "
                            )

                            if pdf_pretty_name == doc_pretty_name:
                                # Encontramos el documento, crear botón de descarga
                                rel_path = os.path.relpath(pdf_path, DOCUMENTS_FOLDER)
                                keyboard.add(
                                    types.InlineKeyboardButton(
                                        f"📥 Descargar {doc_pretty_name}",
                                        callback_data=f"download#{rel_path}",
                                    )
                                )
                                found = True
                                break

                    # Enviar botones solo si hay documentos para descargar
                    if keyboard.keyboard:
                        self.bot.send_message(
                            message.chat.id,
                            "Selecciona un documento para descargar:",
                            reply_markup=keyboard,
                        )

        except Exception as e:
            self.logger.error(f"Error en handle_embedding_search: {str(e)}")
            self.bot.send_message(message.chat.id, "❌ Error al procesar tu búsqueda.")
        finally:
            elapsed = time.perf_counter() - start_time
            self.logger.info(
                f"Tiempo de respuesta de handle_embedding_search: {elapsed:.3f} segundos"
            )
            self.processing_users.remove(user_id)

    def show_help(self, message_or_call):
        """Muestra ayuda del bot UX/UI"""
        chat_id = (
            message_or_call.chat.id
            if hasattr(message_or_call, "chat")
            else message_or_call.message.chat.id
        )

        help_text = (
            "🎨 **Comandos de UX/UI Design:**\n\n"
            "**📋 Consultas especializadas:**\n"
            "• `/design [consulta]` - Principios y teoría del diseño\n"
            "• `/ux [consulta]` - Research y experiencia de usuario\n"
            "• `/ui [consulta]` - Interfaces y patrones visuales\n"
            "• `/tools [consulta]` - Herramientas (Figma, Sketch, etc.)\n\n"
            "**🔍 Búsqueda y consultas:**\n"
            "• `/search [consulta]` - Buscar en recursos especializados\n"
            "• `/ask [pregunta]` - Consultas generales de diseño\n\n"
            "**📚 Recursos por categorías:**\n"
            "Usa los botones del menú para explorar recursos organizados."
        )

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                "🎨 UX Research", callback_data="list_ux_research"
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                "🖼️ UI Patterns", callback_data="list_ui_patterns"
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                "🎯 Design Systems", callback_data="list_design_systems"
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                "📱 Case Studies", callback_data="list_case_studies"
            )
        )

        self.bot.send_message(
            chat_id, help_text, reply_markup=keyboard, parse_mode="Markdown"
        )

    def handle_list(self, call):
        """Maneja listados de recursos por categoría de diseño"""
        category = call.data.replace("list_", "")
        chat_id = call.message.chat.id

        # Mapeo de categorías a carpetas
        folder_mapping = {
            "ux_research": "UX_Research",
            "ui_patterns": "UI_Patterns", 
            "design_systems": "Design_Systems",
            "case_studies": "Case_Studies",
            "tools_guides": "Tools_Guides",
            "accessibility": "Accessibility",
            "prototyping": "Prototyping",
            "user_testing": "User_Testing"
        }

        folder = folder_mapping.get(category)
        if not folder:
            self.bot.answer_callback_query(call.id, "Categoría no disponible")
            return

        try:
            folder_path = os.path.join(DOCUMENTS_FOLDER, folder)
            if not os.path.exists(folder_path):
                self.bot.send_message(chat_id, f"📁 Carpeta {folder} en construcción.\n\n💡 Puedes usar `/search` para buscar en todos los recursos disponibles.")
                return

            pdf_files = [
                f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")
            ]

            if not pdf_files:
                self.bot.send_message(
                    chat_id, f"📚 No hay recursos disponibles en {folder} actualmente.\n\n🔍 Intenta usar `/search [tema]` para encontrar contenido relacionado."
                )
                return

            keyboard = types.InlineKeyboardMarkup()
            for pdf in pdf_files[:10]:  # Limitamos a 10 resultados
                pretty_name = pdf.replace(".pdf", "").replace("_", " ")
                keyboard.add(
                    types.InlineKeyboardButton(
                        f"📄 {pretty_name}", callback_data=f"download#{folder}/{pdf}"
                    )
                )
            keyboard.add(
                types.InlineKeyboardButton("⬅️ Volver", callback_data="back_main")
            )

            category_names = {
                "ux_research": "UX Research",
                "ui_patterns": "UI Patterns",
                "design_systems": "Design Systems", 
                "case_studies": "Case Studies"
            }

            self.bot.send_message(
                chat_id,
                f"📚 **Recursos de {category_names.get(category, folder)}:**",
                reply_markup=keyboard,
                parse_mode="Markdown",
            )
        except Exception as e:
            self.logger.error(f"Error listando recursos de diseño: {e}")
            self.bot.send_message(chat_id, "❌ Error al listar recursos")

    def handle_pdf_download(self, call):
        """Maneja la descarga de documentos PDF"""
        chat_id = call.message.chat.id
        path = call.data.replace("download#", "")

        try:
            file_path = os.path.join(DOCUMENTS_FOLDER, path)
            if not os.path.exists(file_path):
                self.bot.send_message(chat_id, "❌ El archivo solicitado no existe")
                return

            with open(file_path, "rb") as pdf:
                self.bot.send_document(chat_id, pdf)

            self.logger.info(f"Enviado documento: {path}")
        except Exception as e:
            self.logger.error(f"Error enviando PDF: {e}")
            self.bot.send_message(chat_id, "❌ Error al enviar el documento")

    def handle_back(self, call):
        """Maneja botones de regreso"""
        if call.data == "back_main":
            self.show_help(call)
        else:
            self.start(call)

    def handle_message(self, message):
        """Procesa mensajes de texto y comandos especializados en diseño."""

        text = message.text.strip()
        
        # Comandos especializados de diseño
        if text.startswith(("/design", "/ux", "/ui", "/tools")):
            self.handle_general_question(message)
            return
        
        # Responder a mensajes especiales del teclado
        text_lower = text.lower()
        design_categories = {
            "🎨 ux research": "ux_research",
            "🖼️ ui patterns": "ui_patterns", 
            "🎯 design systems": "design_systems",
            "📱 case studies": "case_studies",
            "🛠️ herramientas": "tools_guides",
            "♿ accesibilidad": "accessibility"
        }
        
        for key, category in design_categories.items():
            if text_lower in [key, key.replace("🎨 ", "").replace("🖼️ ", "").replace("🎯 ", "").replace("📱 ", "").replace("🛠️ ", "").replace("♿ ", "")]:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(
                    types.InlineKeyboardButton(
                        "Ver recursos", callback_data=f"list_{category}"
                    )
                )
                category_descriptions = {
                    "ux_research": "🎨 **UX Research** - Métodos de investigación, user personas, journey mapping",
                    "ui_patterns": "🖼️ **UI Patterns** - Componentes, patrones de interfaz, design tokens",
                    "design_systems": "🎯 **Design Systems** - Guías de estilo, componentes reutilizables", 
                    "case_studies": "📱 **Case Studies** - Casos de estudio reales, análisis de diseño",
                    "tools_guides": "🛠️ **Herramientas** - Figma, Sketch, Adobe XD, Prototyping",
                    "accessibility": "♿ **Accesibilidad** - WCAG, diseño inclusivo, mejores prácticas"
                }
                
                self.bot.send_message(
                    message.chat.id,
                    category_descriptions.get(category, f"Recursos de {category}:"),
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
                return

        if text_lower in ["🔍 búsqueda", "búsqueda", "busqueda"]:
            self.bot.send_message(
                message.chat.id,
                "🔍 **Búsqueda especializada en UX/UI:**\n\n"
                "• `/search [tema]` - Buscar en recursos de diseño\n"
                "• `/design [consulta]` - Principios de diseño\n"
                "• `/ux [consulta]` - Experiencia de usuario\n"
                "• `/ui [consulta]` - Interfaces y patrones\n"
                "• `/tools [herramienta]` - Guías de herramientas\n\n"
                "📝 *Ejemplo:* `/search atomic design`",
                parse_mode="Markdown",
            )
            return

        elif text_lower in ["❓ ayuda", "ayuda", "help"]:
            self.show_help(message)
            return

        # Mensajes normales: mostrar comandos disponibles
        self.bot.send_message(
            message.chat.id,
            "🎨 **¿Qué quieres diseñar hoy?**\n\n"
            "**Comandos especializados:**\n"
            "• `/design [consulta]` - Principios y teoría\n"
            "• `/ux [consulta]` - Research y usabilidad\n" 
            "• `/ui [consulta]` - Interfaces y patrones\n"
            "• `/tools [herramienta]` - Guías de Figma, Sketch, etc.\n\n"
            "**Búsqueda:**\n"
            "• `/search [tema]` - Buscar recursos específicos\n"
            "• `/ask [pregunta]` - Consulta general\n\n"
            "💡 *Tip:* Usa los botones del menú para explorar por categorías.",
            parse_mode="Markdown",
        )

    def _is_probable_doi_or_url(self, text):
            """Detecta si el texto es un DOI o URL de artículo científico"""
            import re
            doi_pattern = r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b"
            url_pattern = r"(https?://[^\s]+)"
            return bool(re.search(doi_pattern, text, re.I) or re.search(url_pattern, text, re.I))

    def find_pdf_files(self, folder_path):
        """
        Busca archivos PDF en una carpeta y sus subcarpetas.

        Args:
            folder_path: Ruta de la carpeta donde buscar archivos PDF.

        Returns:
            Lista de rutas de archivos PDF encontrados.
        """
        pdf_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))
        return pdf_files

    def remove_markdown(self, text):
        """
        Elimina completamente el formato Markdown del texto.

        Args:
            text: Texto con posible formato Markdown

        Returns:
            Texto plano sin formato
        """
        import re

        if not text:
            return ""

        # Eliminar bloques de código
        text = re.sub(r"```[\s\S]*?```", "", text)

        # Eliminar formato de negrita y cursiva
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # Negrita
        text = re.sub(r"\*(.*?)\*", r"\1", text)  # Cursiva con asteriscos
        text = re.sub(r"_(.*?)_", r"\1", text)  # Cursiva con guiones bajos

        # Eliminar enlaces, manteniendo el texto
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

        # Eliminar formato de listas
        text = re.sub(r"^\s*[-*+]\s", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*\d+\.\s", "", text, flags=re.MULTILINE)

        # Eliminar encabezados
        text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

        # Eliminar comillas de código en línea
        text = re.sub(r"`(.*?)`", r"\1", text)

        return text


def sanitize_markdown(text):
    """
    Limpia el texto para evitar errores de formato Markdown en Telegram.

    Args:
        text: Texto a limpiar

    Returns:
        Texto limpio con formato Markdown seguro
    """
    if not text:
        return ""

    # Lista de caracteres especiales de Markdown que pueden causar problemas
    special_chars = [
        "_",
        "*",
        "`",
        "[",
        "]",
        "(",
        ")",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]

    # Escapar los caracteres especiales que no formen parte de un formato válido
    result = ""
    i = 0
    in_code_block = False
    in_bold = False
    in_italic = False
    in_link = False

    while i < len(text):
        char = text[i]

        # Manejo de bloques de código
        if i < len(text) - 2 and text[i : i + 3] == "```":
            in_code_block = not in_code_block
            result += "```"
            i += 3
            continue

        # Si estamos dentro de un bloque de código, añadir sin procesar
        if in_code_block:
            result += char
            i += 1
            continue

        # Manejo de negrita
        if i < len(text) - 1 and text[i : i + 2] == "**":
            in_bold = not in_bold
            result += "*"  # Telegram usa un solo asterisco para negrita
            i += 2
            continue

        # Manejo de cursiva
        if char == "_" or (char == "*" and i < len(text) - 1 and text[i + 1] != "*"):
            in_italic = not in_italic
            result += char
            i += 1
            continue

        # Manejo de enlaces
        if char == "[" and not in_link:
            in_link = True
            result += char
            i += 1
            continue
        elif char == "]" and in_link and i < len(text) - 1 and text[i + 1] == "(":
            in_link = False
            result += char
            i += 1
            continue

        # Escapar caracteres especiales que no son parte de formato
        if char in special_chars and not (in_bold or in_italic or in_link):
            result += "\\"

        result += char
        i += 1

    # Arreglar formatos incompletos
    if in_bold:
        result += "*"
    if in_italic:
        result += "_"
    if in_code_block:
        result += "\n```"

    # Dividir mensajes demasiado largos
    if len(result) > 3500:  # Telegram tiene un límite de 4096, dejamos margen
        parts = []
        current_part = ""
        paragraphs = result.split("\n\n")

        for paragraph in paragraphs:
            if len(current_part) + len(paragraph) + 2 > 3500:
                parts.append(current_part)
                current_part = paragraph
            else:
                if current_part:
                    current_part += "\n\n"
                current_part += paragraph

        if current_part:
            parts.append(current_part)

        return parts

    return result
