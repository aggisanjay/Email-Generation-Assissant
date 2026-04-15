"""
email_generator.py — Generates emails using the unified LLM client.
Works with Groq (free) or Ollama (free local).
"""

import config
import prompts
from llm_client import chat


def generate_email(
    intent: str,
    key_facts: str,
    tone: str,
    strategy: str = "a",
) -> str:
    """
    Generate an email for the given intent / facts / tone.

    Args:
        intent:    The purpose of the email.
        key_facts: Semicolon-separated bullet points.
        tone:      Desired tone keyword(s).
        strategy:  'a' for advanced prompt, 'b' for basic prompt.

    Returns:
        The generated email as a string.
    """
    if strategy == "a":
        system_msg = prompts.STRATEGY_A_SYSTEM
        user_msg = prompts.STRATEGY_A_USER_TEMPLATE.format(
            intent=intent, key_facts=key_facts, tone=tone
        )
        model = config.MODEL_A
    else:
        system_msg = prompts.STRATEGY_B_SYSTEM
        user_msg = prompts.STRATEGY_B_USER_TEMPLATE.format(
            intent=intent, key_facts=key_facts, tone=tone
        )
        model = config.MODEL_B

    return chat(
        model=model,
        system_message=system_msg,
        user_message=user_msg,
        temperature=config.GENERATION_PARAMS["temperature"],
        max_tokens=config.GENERATION_PARAMS["max_tokens"],
    )
