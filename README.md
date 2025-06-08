# DesignBot - Tu Mentor Personal de Diseño 🎨✨

Bot especializado en UX/UI Design que utiliza **embeddings vectoriales** e **IA avanzada** para proporcionar asesoría profesional, recursos especializados y mejores prácticas de diseño digital.

## 🚀 Inicio Rápido

```bash
# 1. Clonar el repositorio
git clone <este-repositorio>
cd DesignBot

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 3. Ejecutar script de inicio
./start_bot.sh
```

## 🎯 Características Principales

### 🧠 **Comandos Especializados**
| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/design [consulta]` | Principios y teoría del diseño | `/design jerarquía visual` |
| `/ux [consulta]` | Research y experiencia de usuario | `/ux user personas` |
| `/ui [consulta]` | Interfaces y componentes | `/ui botones accesibles` |
| `/tools [herramienta]` | Guías de herramientas | `/tools Figma components` |

### 🔍 **Búsqueda Inteligente**
- **`/search [tema]`** - Búsqueda semántica en recursos especializados
- **`/ask [pregunta]`** - Consultas generales con IA experta

### 📚 **Biblioteca Organizada**
- **🎨 UX Research** - Metodologías, personas, journey mapping
- **🖼️ UI Patterns** - Componentes, tokens, responsive design
- **🎯 Design Systems** - Atomic design, style guides
- **📱 Case Studies** - Casos reales, redesigns famosos
- **🛠️ Herramientas** - Figma, Sketch, Adobe XD
- **♿ Accesibilidad** - WCAG, diseño inclusivo

## 🛠️ Tecnología

- **🤖 Fireworks AI** - LLM especializado en UX/UI
- **🔍 Embeddings vectoriales** - Búsqueda semántica avanzada
- **📄 Procesamiento PDF** - Extracción inteligente de contenido
- **⚡ Índice sklearn** - Búsquedas ultrarrápidas
- **📱 Telegram Bot API** - Interfaz conversacional

## ⚙️ Configuración Detallada

### 📋 **Requisitos**
- Python 3.8+
- Token de Telegram Bot (@BotFather)
- API Key de Fireworks AI

### 🔧 **Instalación Manual**
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar bot
cd Bot && python main.py
```

### 🔑 **Variables de Entorno (.env)**
```bash
TOKEN=tu_token_telegram          # De @BotFather
FIRE=tu_api_key_fireworks       # De Fireworks AI
BOT_NAME=DesignBot              # Nombre del bot
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING
```

## 📁 Estructura del Proyecto

```
DesignBot/
├── 📄 README.md                    # Documentación principal
├── 📄 requirements.txt             # Dependencias Python
├── 📄 .env.example                 # Plantilla de configuración
├── 🚀 start_bot.sh                 # Script de inicio rápido
├── 📁 Bot/                         # Código principal
│   ├── 🤖 main.py                  # Punto de entrada
│   ├── 🧠 bot_handler.py           # Lógica del bot
│   ├── ⚙️  constants.py            # Configuraciones
│   ├── 📝 logger.py                # Sistema de logs
│   ├── 📁 ai_embedding/            # Motor de IA
│   │   ├── 🔬 ai.py                # Generación de respuestas
│   │   └── 📊 extract.py           # Procesamiento de PDFs
│   └── 📁 Design_Resources/        # Biblioteca de recursos
│       ├── 🎨 UX_Research/
│       ├── 🖼️  UI_Patterns/
│       ├── 🎯 Design_Systems/
│       ├── 📱 Case_Studies/
│       ├── 🛠️  Tools_Guides/
│       ├── ♿ Accessibility/
│       ├── 🔧 Prototyping/
│       ├── 👥 User_Testing/
│       ├── 📐 Wireframing/
│       └── 🗂️  Information_Architecture/
├── 📁 data/                        # Embeddings e índices (auto-generado)
└── 📁 logs/                        # Archivos de log (auto-generado)
```

## 🎨 Ejemplos de Uso Avanzado

### 💬 **Conversaciones Típicas**

**Usuario:** `/ux cómo validar user personas`
**Bot:** *Respuesta detallada sobre métodos de validación, métricas, herramientas de testing...*

**Usuario:** `/search atomic design`
**Bot:** *Búsqueda en recursos + respuesta contextualizada con citas específicas*

**Usuario:** `/tools Figma auto layout`
**Bot:** *Guías paso a paso, mejores prácticas, tips avanzados...*

### 📊 **Flujo de Trabajo Típico**
1. **Explorar recursos** → Usar botones del menú
2. **Buscar específico** → `/search [tema]`
3. **Profundizar** → Comandos especializados (`/ux`, `/ui`, `/design`)
4. **Descargar recursos** → Botones de descarga automática

## 🚀 Características Avanzadas

### 🎯 **IA Especializada**
- **Contexto de diseño** - Respuestas enfocadas en UX/UI
- **Herramientas específicas** - Menciona Figma, Sketch, Adobe XD según contexto
- **Mejores prácticas** - Integra tendencias actuales y estándares
- **Ejemplos reales** - Casos de uso del mundo real

### 📖 **Gestión de Recursos**
- **Auto-indexación** - Procesa PDFs automáticamente
- **Búsqueda semántica** - Encuentra conceptos relacionados
- **Citas precisas** - Referencias con páginas específicas
- **Descargas directas** - Acceso inmediato a recursos

### 🔍 **Búsqueda Inteligente**
- **Embeddings optimizados** - Terminología de diseño especializada
- **Resultados contextuales** - Filtrado por categoría
- **Relevancia semántica** - Encuentra conceptos relacionados
- **Referencias cruzadas** - Conecta ideas entre documentos

## 📚 Agregar Contenido

### 📄 **Agregar PDFs**
1. Coloca archivos PDF en las carpetas correspondientes de `Design_Resources/`
2. Reinicia el bot para auto-indexar el contenido
3. Los nuevos recursos estarán disponibles inmediatamente

### 🏷️ **Categorías Recomendadas**
- **UX_Research**: Métodos, templates, case studies de research
- **UI_Patterns**: Componentes, design tokens, responsive patterns
- **Design_Systems**: Atomic design, style guides, documentation
- **Tools_Guides**: Tutoriales de Figma, Sketch, Adobe XD
- **Accessibility**: WCAG, inclusive design, testing methods

## 🤝 Contribuir

### 🎯 **Áreas Prioritarias**
- [ ] **📚 Recursos de calidad** - PDFs, guías, case studies
- [ ] **🔧 Mejoras de IA** - Prompts más específicos
- [ ] **🎨 Nuevas categorías** - Motion design, VR/AR UX
- [ ] **🔗 Integraciones** - APIs de Dribbble, Behance

### 📝 **Proceso de Contribución**
```bash
# 1. Fork del repositorio
git fork <este-repo>

# 2. Crear rama feature
git checkout -b feature/nueva-funcionalidad

# 3. Hacer cambios y commit
git commit -am "Añadir nueva funcionalidad"

# 4. Push y Pull Request
git push origin feature/nueva-funcionalidad
```

## 🆘 Resolución de Problemas

### ❌ **Errores Comunes**

**"No module named 'telebot'"**
```bash
pip install pyTelegramBotAPI
```

**"API Key inválida"**
- Verificar .env con TOKEN y FIRE correctos
- Comprobar que no haya espacios extra

**"No se encuentran documentos"**
- Verificar que existan PDFs en Design_Resources/
- Reiniciar bot para re-indexar

### 📊 **Logs y Debugging**
```bash
# Ver logs en tiempo real
tail -f Bot/logs/bot_log.log

# Logs de IA y embeddings
tail -f Bot/logs/ai.log
tail -f Bot/logs/data.log
```

## 📈 Roadmap

### 🎯 **V1.1 - Próximas Características**
- [ ] **🎨 Generación de imágenes** - Mockups y wireframes automáticos
- [ ] **📊 Analytics de uso** - Estadísticas de consultas populares
- [ ] **🔄 Sync con Figma** - Integración directa con archivos
- [ ] **👥 Colaboración** - Compartir hallazgos entre usuarios

### 🚀 **V2.0 - Visión a Largo Plazo**
- [ ] **🤖 Assistant mode** - Conversaciones contextuales largas
- [ ] **📱 Plugin mobile** - App nativa complementaria
- [ ] **🎓 Learning paths** - Rutas de aprendizaje personalizadas
- [ ] **🌐 Web interface** - Dashboard complementario

## 📞 Soporte

- **🐛 Issues**: Reportar bugs en GitHub Issues
- **💡 Ideas**: Sugerir mejoras en Discussions
- **📧 Contact**: Para consultas específicas

---

**🎨 Transformando ideas en experiencias excepcionales, un diseño a la vez.**

*Desarrollado con ❤️ para la comunidad de UX/UI Design*
