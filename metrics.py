"""
metrics.py — Three custom evaluation metrics for the Email Generation
Assistant. Uses the free LLM client (Groq/Ollama) for judge calls.

╔══════════════════════════════════════════════════════════════════════╗
║  METRIC 1 — Fact Inclusion Score (0-100)                           ║
║  METRIC 2 — Tone Alignment Score (0-100)                           ║
║  METRIC 3 — Professional Quality Score (0-100)                     ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import re
import json
import textwrap
import textstat
import config
from llm_client import chat


# ───────────────────────────────────────────────────────────────────
# Helper: call the judge LLM
# ───────────────────────────────────────────────────────────────────

def _judge(system: str, user: str) -> str:
    """Call the judge model with low temperature for consistency."""
    return chat(
        model=config.JUDGE_MODEL,
        system_message=system,
        user_message=user,
        temperature=config.JUDGE_PARAMS["temperature"],
        max_tokens=config.JUDGE_PARAMS["max_tokens"],
    )


def _parse_json(raw: str) -> dict | list:
    """Extract JSON from LLM response, handling markdown fences."""
    raw_clean = re.sub(r"```json\s*|```", "", raw).strip()
    # Try to find JSON in the response
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = raw_clean.find(start_char)
        end = raw_clean.rfind(end_char)
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw_clean[start:end + 1])
            except json.JSONDecodeError:
                continue
    raise json.JSONDecodeError("No valid JSON found", raw_clean, 0)


# ══════════════════════════════════════════════════════════════════
# METRIC 1 — Fact Inclusion Score
# ══════════════════════════════════════════════════════════════════
# Definition: Measures the degree to which every key fact supplied by
# the user is accurately and explicitly present in the generated email.
#
# Logic:
#   1. key_facts string is split on ";" → N individual facts.
#   2. An LLM judge checks each fact: PRESENT or MISSING.
#   3. Score = (# PRESENT / N) × 100
#
# Why LLM-as-a-Judge? Facts may be paraphrased ("\$500K" → "\$500,000").
# ══════════════════════════════════════════════════════════════════

FACT_JUDGE_SYSTEM = textwrap.dedent("""\
    You are a precise fact-verification auditor.
    You will receive a list of FACTS and a generated EMAIL.
    For EACH fact, determine if it is faithfully represented in the email.
    Respond ONLY with valid JSON — an array of objects:
    [
      {"fact": "<fact text>", "status": "PRESENT" or "MISSING", "reason": "<brief>"}
    ]
    Do not include any other text outside the JSON.
""")


def fact_inclusion_score(key_facts: str, generated_email: str) -> dict:
    facts = [f.strip() for f in key_facts.split(";") if f.strip()]
    fact_list_str = "\n".join(f"- {f}" for f in facts)

    user_prompt = f"FACTS:\n{fact_list_str}\n\nEMAIL:\n{generated_email}"
    raw = _judge(FACT_JUDGE_SYSTEM, user_prompt)

    try:
        details = _parse_json(raw)
    except json.JSONDecodeError:
        details = [{"fact": f, "status": "MISSING", "reason": "parse error"}
                    for f in facts]

    present = sum(1 for d in details if d.get("status", "").upper() == "PRESENT")
    score = round((present / max(len(facts), 1)) * 100, 1)
    return {"score": score, "details": details}


# ══════════════════════════════════════════════════════════════════
# METRIC 2 — Tone Alignment Score
# ══════════════════════════════════════════════════════════════════
# Definition: Measures how well the generated email matches the
# user-requested tone.
#
# Logic:
#   1. LLM judge rates tone match on 1–5 Likert rubric.
#   2. Normalized: ((likert - 1) / 4) × 100
#
# Rubric:
#   5 — Perfect match throughout.
#   4 — Mostly accurate, minor deviations.
#   3 — Partially correct but inconsistent.
#   2 — Largely incorrect.
#   1 — Entirely wrong tone.
# ══════════════════════════════════════════════════════════════════

TONE_JUDGE_SYSTEM = textwrap.dedent("""\
    You are an expert editorial tone analyst.
    You will receive a REQUESTED TONE and a generated EMAIL.
    Rate how well the email matches the requested tone:
      5 — Perfect match throughout.
      4 — Mostly accurate, minor deviations.
      3 — Partially correct but noticeably inconsistent.
      2 — Largely incorrect, only glimpses of the target tone.
      1 — Entirely wrong or inappropriate tone.
    Respond ONLY with valid JSON:
    {"likert": <int 1-5>, "justification": "<brief explanation>"}
    Do not include any other text outside the JSON.
""")


def tone_alignment_score(tone: str, generated_email: str) -> dict:
    user_prompt = f"REQUESTED TONE: {tone}\n\nEMAIL:\n{generated_email}"
    raw = _judge(TONE_JUDGE_SYSTEM, user_prompt)

    try:
        result = _parse_json(raw)
    except json.JSONDecodeError:
        result = {"likert": 3, "justification": "parse error — default mid"}

    likert = int(result.get("likert", 3))
    likert = max(1, min(5, likert))
    score = round(((likert - 1) / 4) * 100, 1)
    return {
        "score": score,
        "likert": likert,
        "justification": result.get("justification", ""),
    }


# ══════════════════════════════════════════════════════════════════
# METRIC 3 — Professional Quality Score
# ══════════════════════════════════════════════════════════════════
# Definition: Composite metric evaluating grammar/fluency, structural
# completeness, and conciseness.
#
# Sub-scores (equally weighted):
#   A. Structure (heuristic): Subject line, greeting, closing, paragraphs
#   B. Readability (heuristic): Flesch score + word count check
#   C. Grammar (LLM judge): 1-5 Likert → normalized
#
# Final = (A + B + C) / 3
# ══════════════════════════════════════════════════════════════════

GRAMMAR_JUDGE_SYSTEM = textwrap.dedent("""\
    You are an expert copy-editor.
    Rate the following EMAIL for grammar and fluency on a 1-5 scale:
      5 — Flawless grammar and natural fluency.
      4 — Very minor issues, still reads well.
      3 — A few noticeable errors or awkward phrasing.
      2 — Multiple errors that impede readability.
      1 — Severely broken grammar; very hard to read.
    Respond ONLY with valid JSON:
    {"likert": <int 1-5>, "issues": "<brief list of issues or 'none'>"}
    Do not include any other text outside the JSON.
""")


def _structure_subscore(email: str) -> float:
    """Heuristic structural completeness check."""
    score = 0
    if re.search(r"(?i)^subject\s*:", email, re.MULTILINE):
        score += 25
    if re.search(
        r"(?i)^(dear|hi|hey|hello|good morning|good afternoon|greetings)",
        email, re.MULTILINE,
    ):
        score += 25
    if re.search(r"(?i)(regards|sincerely|cheers|best|thank|warm|yours)", email):
        score += 25
    paragraphs = [p.strip() for p in email.split("\n\n") if p.strip()]
    if len(paragraphs) >= 3:
        score += 25
    return float(score)


def _readability_subscore(email: str) -> float:
    """Readability and conciseness heuristic."""
    body = re.sub(r"(?i)^subject\s*:.*\n*", "", email).strip()
    words = body.split()
    word_count = len(words)

    fre = textstat.flesch_reading_ease(body) if body else 50.0
    if 50 <= fre <= 70:
        read_score = 100.0
    elif fre < 50:
        read_score = max(0, 100 - (50 - fre) * 2)
    else:
        read_score = max(0, 100 - (fre - 70) * 2)

    if word_count < 40:
        read_score -= 25
    if word_count > 300:
        read_score -= 25

    return max(0.0, min(100.0, read_score))


def _grammar_subscore(email: str) -> dict:
    """LLM-as-a-Judge grammar evaluation."""
    raw = _judge(GRAMMAR_JUDGE_SYSTEM, f"EMAIL:\n{email}")
    try:
        result = _parse_json(raw)
    except json.JSONDecodeError:
        result = {"likert": 3, "issues": "parse error — default mid"}
    likert = max(1, min(5, int(result.get("likert", 3))))
    score = round(((likert - 1) / 4) * 100, 1)
    return {"score": score, "likert": likert, "issues": result.get("issues", "")}


def professional_quality_score(generated_email: str) -> dict:
    structure = _structure_subscore(generated_email)
    readability = _readability_subscore(generated_email)
    grammar_result = _grammar_subscore(generated_email)
    grammar = grammar_result["score"]

    composite = round((structure + readability + grammar) / 3, 1)
    return {
        "score": composite,
        "structure": structure,
        "readability": readability,
        "grammar": grammar,
        "grammar_details": grammar_result,
    }
