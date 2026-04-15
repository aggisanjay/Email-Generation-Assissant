"""
config.py — Configuration for free LLM providers (Groq or Ollama).
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Provider Selection ────────────────────────────────────────────────
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()  # "groq" or "ollama"

# ── Groq (Free Cloud API) ────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Groq free-tier models
GROQ_MODEL_STRONG = "llama-3.3-70b-versatile"    # Strategy A
GROQ_MODEL_LIGHT = "llama-3.1-8b-instant"         # Strategy B
GROQ_MODEL_JUDGE = "llama-3.3-70b-versatile"       # Evaluation judge

# ── Ollama (Free Local) ──────────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Ollama model names (must be pulled first: ollama pull <name>)
OLLAMA_MODEL_STRONG = "llama3.1:70b"               # Strategy A
OLLAMA_MODEL_LIGHT = "llama3.1:8b"                  # Strategy B
OLLAMA_MODEL_JUDGE = "llama3.1:70b"                 # Evaluation judge

# ── Resolved model names based on provider ────────────────────────────
if LLM_PROVIDER == "groq":
    if not GROQ_API_KEY:
        raise EnvironmentError(
            "Set GROQ_API_KEY in .env — get a free key at https://console.groq.com"
        )
    MODEL_A = GROQ_MODEL_STRONG
    MODEL_B = GROQ_MODEL_LIGHT
    JUDGE_MODEL = GROQ_MODEL_JUDGE
else:
    MODEL_A = OLLAMA_MODEL_STRONG
    MODEL_B = OLLAMA_MODEL_LIGHT
    JUDGE_MODEL = OLLAMA_MODEL_JUDGE

# ── Generation parameters ─────────────────────────────────────────────
GENERATION_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 1024,
}

JUDGE_PARAMS = {
    "temperature": 0.0,
    "max_tokens": 1024,
}

print(f"[Config] Provider: {LLM_PROVIDER}")
print(f"[Config] Model A (strong): {MODEL_A}")
print(f"[Config] Model B (light):  {MODEL_B}")
print(f"[Config] Judge model:      {JUDGE_MODEL}")
