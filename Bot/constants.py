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
    "TOOLS_GUIDES": "Tools & Guides"
}

# Mapeo de categorías a emojis más claros y accesibles
CATEGORY_EMOJIS = {
    "UX_RESEARCH": "🔬",          # Microscopio para investigación
    "UI_PATTERNS": "🎨",          # Paleta para patrones visuales  
    "DESIGN_SYSTEMS": "🎯",       # Diana para sistemas organizados
    "TOOLS_GUIDES": "🛠️"          # Herramientas
}

# Descripciones claras para cada categoría (para mejorar accesibilidad)
CATEGORY_DESCRIPTIONS = {
    "UX_RESEARCH": "Investigación de usuarios, métodos, análisis",
    "UI_PATTERNS": "Componentes, interfaces, patrones visuales",
    "DESIGN_SYSTEMS": "Guías de estilo, bibliotecas de componentes", 
    "TOOLS_GUIDES": "Tutoriales de Figma, Sketch, Adobe XD"
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
