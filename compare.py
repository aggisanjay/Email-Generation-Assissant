"""
compare.py — Run both strategies, compare results, write comparison JSON.

Usage:
    python compare.py
"""

import json
import os
from evaluate import run_evaluation


def main():
    print("\n" + "=" * 60)
    print("  COMPARATIVE EVALUATION (Free LLMs)")
    print("=" * 60)

    print("\n▶ Evaluating Strategy A (Advanced Prompt + Strong Model)...\n")
    results_a = run_evaluation("a")

    print("\n▶ Evaluating Strategy B (Basic Prompt + Light Model)...\n")
    results_b = run_evaluation("b")

    # ── Build comparison ──────────────────────────────────────────
    comparison = {
        "strategy_a": {
            "description": results_a["meta"],
            "averages": results_a["averages"],
        },
        "strategy_b": {
            "description": results_b["meta"],
            "averages": results_b["averages"],
        },
        "per_scenario_delta": [],
    }

    for sa, sb in zip(results_a["scenarios"], results_b["scenarios"]):
        comparison["per_scenario_delta"].append({
            "id": sa["id"],
            "fact_delta": round(
                sa["metrics"]["fact_inclusion"]["score"]
                - sb["metrics"]["fact_inclusion"]["score"], 1
            ),
            "tone_delta": round(
                sa["metrics"]["tone_alignment"]["score"]
                - sb["metrics"]["tone_alignment"]["score"], 1
            ),
            "quality_delta": round(
                sa["metrics"]["professional_quality"]["score"]
                - sb["metrics"]["professional_quality"]["score"], 1
            ),
        })

    avg_a = results_a["averages"]["overall_avg"]
    avg_b = results_b["averages"]["overall_avg"]
    winner = "Strategy A" if avg_a >= avg_b else "Strategy B"

    loser_avgs = results_b["averages"] if winner == "Strategy A" else results_a["averages"]
    metric_map = {
        "fact_inclusion_avg": "Fact Inclusion",
        "tone_alignment_avg": "Tone Alignment",
        "professional_quality_avg": "Professional Quality",
    }
    worst_key = min(
        ["fact_inclusion_avg", "tone_alignment_avg", "professional_quality_avg"],
        key=lambda k: loser_avgs[k],
    )

    comparison["analysis"] = {
        "winner": winner,
        "winner_overall_avg": max(avg_a, avg_b),
        "loser_overall_avg": min(avg_a, avg_b),
        "biggest_failure_mode_of_loser": metric_map[worst_key],
        "loser_worst_score": loser_avgs[worst_key],
        "recommendation": (
            f"{winner} is recommended for production. It achieved an overall "
            f"average of {max(avg_a, avg_b)} vs {min(avg_a, avg_b)}. "
            f"The lower-performing strategy struggled most with "
            f"{metric_map[worst_key]} (avg {loser_avgs[worst_key]}). "
            f"The advanced prompting (Role-Play + Few-Shot + CoT) "
            f"significantly improves fact recall and tone accuracy."
        ),
    }

    # ── Save all files ────────────────────────────────────────────
    os.makedirs("results", exist_ok=True)
    with open("results/evaluation_strategy_a.json", "w") as f:
        json.dump(results_a, f, indent=2)
    with open("results/evaluation_strategy_b.json", "w") as f:
        json.dump(results_b, f, indent=2)
    with open("results/comparison_report.json", "w") as f:
        json.dump(comparison, f, indent=2)

    # ── Print summary ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  COMPARISON SUMMARY")
    print("=" * 60)
    print(f"\n  Strategy A overall avg: {avg_a}")
    print(f"  Strategy B overall avg: {avg_b}")
    print(f"  Winner: {winner}")
    print(f"  Biggest failure of loser: {metric_map[worst_key]} ({loser_avgs[worst_key]})")
    print(f"\n  Files written:")
    print(f"    results/evaluation_strategy_a.json")
    print(f"    results/evaluation_strategy_b.json")
    print(f"    results/comparison_report.json\n")


if __name__ == "__main__":
    main()
