"""
evaluate.py — Run all 10 scenarios through one strategy, compute metrics,
and write results to JSON.

Usage:
    python evaluate.py --strategy a
    python evaluate.py --strategy b
"""

import argparse
import json
import os
import time
from datetime import datetime, timezone

from email_generator import generate_email
from test_scenarios import SCENARIOS
from metrics import (
    fact_inclusion_score,
    tone_alignment_score,
    professional_quality_score,
)
import config


def run_evaluation(strategy: str) -> dict:
    model_name = config.MODEL_A if strategy == "a" else config.MODEL_B
    prompt_type = (
        "Advanced (Role-Play + Few-Shot + CoT)"
        if strategy == "a"
        else "Basic (single instruction)"
    )

    results = {
        "meta": {
            "strategy": strategy.upper(),
            "provider": config.LLM_PROVIDER,
            "model": model_name,
            "prompt_type": prompt_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "metric_definitions": {
            "fact_inclusion_score": {
                "name": "Fact Inclusion Score",
                "range": "0-100",
                "focus": "Information Recall / Specificity",
                "logic": (
                    "Key facts are split by semicolons. An LLM judge checks "
                    "each fact against the email (PRESENT/MISSING). "
                    "Score = (present / total) × 100."
                ),
            },
            "tone_alignment_score": {
                "name": "Tone Alignment Score",
                "range": "0-100",
                "focus": "Tone Accuracy",
                "logic": (
                    "An LLM judge rates tone match on a 1-5 Likert rubric. "
                    "Normalized: ((likert - 1) / 4) × 100."
                ),
            },
            "professional_quality_score": {
                "name": "Professional Quality Score",
                "range": "0-100",
                "focus": "Grammar, Structure, Conciseness",
                "logic": (
                    "Composite of 3 equally weighted sub-scores: "
                    "(A) Structural completeness heuristic, "
                    "(B) Readability & word-count heuristic, "
                    "(C) Grammar fluency via LLM-as-a-Judge."
                ),
            },
        },
        "scenarios": [],
        "averages": {},
    }

    fact_scores = []
    tone_scores = []
    quality_scores = []

    for scenario in SCENARIOS:
        print(f"  ▸ Scenario {scenario['id']}... ", end="", flush=True)

        # Rate limiting for Groq free tier (30 req/min)
        if config.LLM_PROVIDER == "groq":
            time.sleep(3)

        generated = generate_email(
            intent=scenario["intent"],
            key_facts=scenario["key_facts"],
            tone=scenario["tone"],
            strategy=strategy,
        )

        # Small delays between judge calls for rate limiting
        if config.LLM_PROVIDER == "groq":
            time.sleep(2)
        m1 = fact_inclusion_score(scenario["key_facts"], generated)

        if config.LLM_PROVIDER == "groq":
            time.sleep(2)
        m2 = tone_alignment_score(scenario["tone"], generated)

        if config.LLM_PROVIDER == "groq":
            time.sleep(2)
        m3 = professional_quality_score(generated)

        fact_scores.append(m1["score"])
        tone_scores.append(m2["score"])
        quality_scores.append(m3["score"])

        results["scenarios"].append({
            "id": scenario["id"],
            "intent": scenario["intent"],
            "tone": scenario["tone"],
            "key_facts": scenario["key_facts"],
            "generated_email": generated,
            "reference_email": scenario["reference_email"],
            "metrics": {
                "fact_inclusion": m1,
                "tone_alignment": m2,
                "professional_quality": m3,
            },
        })
        print(
            f"Fact={m1['score']}  Tone={m2['score']}  "
            f"Quality={m3['score']}"
        )

    n = len(fact_scores)
    results["averages"] = {
        "fact_inclusion_avg": round(sum(fact_scores) / n, 1),
        "tone_alignment_avg": round(sum(tone_scores) / n, 1),
        "professional_quality_avg": round(sum(quality_scores) / n, 1),
        "overall_avg": round(
            (sum(fact_scores) + sum(tone_scores) + sum(quality_scores))
            / (3 * n),
            1,
        ),
    }

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strategy", choices=["a", "b"], default="a",
        help="Prompting strategy: a=advanced, b=basic",
    )
    args = parser.parse_args()

    print(f"\n{'=' * 60}")
    print(f"  Running evaluation — Strategy {args.strategy.upper()}")
    print(f"  Provider: {config.LLM_PROVIDER}")
    print(f"{'=' * 60}\n")

    results = run_evaluation(args.strategy)

    os.makedirs("results", exist_ok=True)
    out_path = f"results/evaluation_strategy_{args.strategy}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"  Averages — Strategy {args.strategy.upper()}")
    print(f"{'=' * 60}")
    for k, v in results["averages"].items():
        print(f"  {k}: {v}")
    print(f"\n  Results written to {out_path}\n")


if __name__ == "__main__":
    main()
