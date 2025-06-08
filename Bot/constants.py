# constants.py
import os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


EMBEDDINGS_FILE = os.path.join(ROOT_DIR, "Bot", "data", "embeddings_data.pkl")
INDEX_FILE = os.path.join(ROOT_DIR, "Bot", "data", "vector_index.pkl")
DOCUMENTS_FOLDER = os.path.join(ROOT_DIR, "Bot", "Design_Resources")
LOGS_FOLDER = os.path.join(ROOT_DIR, "Bot", "logs")

# Categorías esenciales de recursos de diseño UX/UI (simplificadas y más accesibles)
DESIGN_CATEGORIES = {
    "UX_RESEARCH": "UX Research",
    "UI_PATTERNS": "UI Patterns", 
    "DESIGN_SYSTEMS": "Design Systems",
    "CASE_STUDIES": "Case Studies",
    "TOOLS_GUIDES": "Tools & Guides",
    "ACCESSIBILITY": "Accessibility"
}

# Mapeo de categorías a emojis más claros y accesibles
CATEGORY_EMOJIS = {
    "UX_RESEARCH": "🔍",          # Lupa para investigación
    "UI_PATTERNS": "🎨",          # Paleta para patrones visuales  
    "DESIGN_SYSTEMS": "🎯",       # Diana para sistemas organizados
    "CASE_STUDIES": "📋",         # Clipboard para casos de estudio
    "TOOLS_GUIDES": "🛠️",         # Herramientas
    "ACCESSIBILITY": "♿"          # Accesibilidad universal
}

# Descripciones claras para cada categoría (para mejorar accesibilidad)
CATEGORY_DESCRIPTIONS = {
    "UX_RESEARCH": "Investigación de usuarios, métodos, análisis",
    "UI_PATTERNS": "Componentes, interfaces, patrones visuales",
    "DESIGN_SYSTEMS": "Guías de estilo, bibliotecas de componentes", 
    "CASE_STUDIES": "Casos reales, análisis de productos",
    "TOOLS_GUIDES": "Tutoriales de Figma, Sketch, Adobe XD",
    "ACCESSIBILITY": "Diseño inclusivo, WCAG, mejores prácticas"
}

# Herramientas de diseño soportadas
DESIGN_TOOLS = [
    "Figma",
    "Sketch",
    "Adobe XD", 
    "InVision",
    "Principle",
    "Framer",
    "Axure",
    "Balsamiq",
    "Marvel",
    "Zeplin"
]
