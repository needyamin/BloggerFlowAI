"""App configuration. Credentials in credentials/."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_DIR = BASE_DIR / "credentials"

# --- Credentials (place credentials.json & token.json in credentials/) ---
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE") or str(CREDENTIALS_DIR / "credentials.json")
TOKEN_FILE = os.getenv("TOKEN_FILE") or str(CREDENTIALS_DIR / "token.json")

# --- Blogger ---
BLOGGER_BLOG_ID = os.getenv("BLOGGER_BLOG_ID", "3422137415075355570")

# --- AI APIs (failover: OpenAI → Gemini) ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# --- Blog post limits ---
BLOG_POST_MIN_WORDS = int(os.getenv("BLOG_POST_MIN_WORDS", "3000"))
FORCE_POST = os.getenv("FORCE_POST", "false").lower() in ("1", "true", "yes")  # skip min-word check
BLOG_POST_MAX_WORDS = int(os.getenv("BLOG_POST_MAX_WORDS", "12000"))
POST_TITLE_MAX_CHARS = int(os.getenv("POST_TITLE_MAX_CHARS", "100"))

# --- AI output (tokens & structure) ---
AI_MIN_TOKENS = int(os.getenv("AI_MIN_TOKENS", "1024"))
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "4096"))
OUTLINE_SECTIONS = int(os.getenv("OUTLINE_SECTIONS", "15"))
SECTION_WORDS = int(os.getenv("SECTION_WORDS", "100"))

# --- Run mode: "scheduler" (daily at 9:00) | "direct" (post once now) ---
RUN_MODE = os.getenv("RUN_MODE", "scheduler").lower().strip()  # scheduler | direct

# --- Generation phase labels (for progress messages) ---
LOG_VERBOSE = os.getenv("LOG_VERBOSE", "true").lower() in ("1", "true", "yes")
MSG_START = os.getenv("MSG_START", "[+] Starting MASSIVE generation for: {topic}")
MSG_PHASE1 = os.getenv("MSG_PHASE1", "[+] PHASE 1: Generating {n}-section outline...")
MSG_OUTLINE_READY = os.getenv("MSG_OUTLINE_READY", "[+] Outline ready with {n} sections.")
MSG_PHASE2_HEADER = os.getenv("MSG_PHASE2_HEADER", "[+] PHASE 2: Generating Header and Introduction...")
MSG_PHASE2_SECTION = os.getenv("MSG_PHASE2_SECTION", "[+] PHASE 2: Generating section {i}/{total}: {section}")
MSG_COMPLETE = os.getenv("MSG_COMPLETE", "[+] MASSIVE Generation Complete! {wc} words (target: {min}-{max})")
FIRST_SECTION_NAME = os.getenv("FIRST_SECTION_NAME", "Introduction and Title")

# --- Topics ---
TOPIC = os.getenv("TOPIC")
TOPICS = [
    "Education", "Scholarship Abroad", "Latest Technology News",
    "Scholarship in USA/Japan/UK", "Global Breaking News", "Viral News", "Secret Societies",
]
