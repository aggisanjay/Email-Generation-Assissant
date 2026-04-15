"""
llm_client.py — Unified LLM client that works with Groq (free cloud)
or Ollama (free local). Both use OpenAI-compatible chat format.
"""

import json
import requests
import config

# ── Groq client (uses groq Python SDK) ───────────────────────────────
_groq_client = None

def _get_groq_client():
    global _groq_client
    if _groq_client is None:
        from groq import Groq
        _groq_client = Groq(api_key=config.GROQ_API_KEY)
    return _groq_client


def _call_groq(model: str, messages: list, temperature: float, max_tokens: int) -> str:
    client = _get_groq_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


# ── Ollama client (REST API) ─────────────────────────────────────────

def _call_ollama(model: str, messages: list, temperature: float, max_tokens: int) -> str:
    url = f"{config.OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()["message"]["content"].strip()
    except requests.ConnectionError:
        raise ConnectionError(
            f"Cannot connect to Ollama at {config.OLLAMA_BASE_URL}. "
            "Make sure Ollama is running: `ollama serve`"
        )
    except requests.HTTPError as e:
        raise RuntimeError(f"Ollama error: {e.response.text}")


# ── Unified interface ─────────────────────────────────────────────────

def chat(
    model: str,
    system_message: str,
    user_message: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    """
    Send a chat completion request to the configured LLM provider.

    Args:
        model: Model name (resolved from config).
        system_message: System prompt.
        user_message: User prompt.
        temperature: Sampling temperature.
        max_tokens: Max response tokens.

    Returns:
        The assistant's response as a string.
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    if config.LLM_PROVIDER == "groq":
        return _call_groq(model, messages, temperature, max_tokens)
    else:
        return _call_ollama(model, messages, temperature, max_tokens)
