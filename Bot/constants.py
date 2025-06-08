# constants.py
import os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


EMBEDDINGS_FILE = os.path.join(ROOT_DIR, "Bot", "data", "embeddings_data.pkl")
INDEX_FILE = os.path.join(ROOT_DIR, "Bot", "data", "vector_index.pkl")
DOCUMENTS_FOLDER = os.path.join(ROOT_DIR, "Bot", "Design_Resources")
LOGS_FOLDER = os.path.join(ROOT_DIR, "Bot", "logs")

# Categorías de recursos de diseño UX/UI
DESIGN_CATEGORIES = {
    "UX_RESEARCH": "UX Research",
    "UI_PATTERNS": "UI Patterns", 
    "DESIGN_SYSTEMS": "Design Systems",
    "CASE_STUDIES": "Case Studies",
    "TOOLS_GUIDES": "Tools & Guides",
    "ACCESSIBILITY": "Accessibility",
    "PROTOTYPING": "Prototyping",
    "USER_TESTING": "User Testing",
    "WIREFRAMING": "Wireframing",
    "INFORMATION_ARCHITECTURE": "Information Architecture"
}

# Mapeo de categorías a emojis para el bot
CATEGORY_EMOJIS = {
    "UX_RESEARCH": "🎨",
    "UI_PATTERNS": "🖼️", 
    "DESIGN_SYSTEMS": "🎯",
    "CASE_STUDIES": "📱",
    "TOOLS_GUIDES": "🛠️",
    "ACCESSIBILITY": "♿",
    "PROTOTYPING": "🔧",
    "USER_TESTING": "👥",
    "WIREFRAMING": "📐",
    "INFORMATION_ARCHITECTURE": "🗂️"
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
