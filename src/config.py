"""
AGL — Autonomous Legal Contract Negotiator
Configuration centrale du projet.
Toutes les valeurs sensibles viennent du fichier .env
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── LLM ─────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL      = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

# ─── Paramètres de négociation ────────────────────────────────────────────────
MAX_TURNS             = int(os.getenv("MAX_TURNS", "10"))
MIN_TURNS             = int(os.getenv("MIN_TURNS", "3"))
CONVERGENCE_THRESHOLD = float(os.getenv("CONVERGENCE_THRESHOLD", "0.92"))
FLATLINE_TURNS        = int(os.getenv("FLATLINE_TURNS", "3"))

# ─── Chemins de sortie ────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR  = os.path.join(BASE_DIR, "output")
ASSETS_DIR  = os.path.join(BASE_DIR, "assets")
DOCX_OUTPUT = os.path.join(OUTPUT_DIR, "negotiated_nda.docx")

# ─── Embedding (convergence evaluator) ───────────────────────────────────────
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)