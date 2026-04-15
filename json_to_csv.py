import json
import csv
import os

def json_to_csv():
    results_dir = "results"
    files = ["evaluation_strategy_a.json", "evaluation_strategy_b.json"]
    output_file = os.path.join(results_dir, "evaluation_summary.csv")

    if not os.path.exists(results_dir):
        print(f"Error: {results_dir} directory not found.")
        return

    csv_data = []
    headers = [
        "Strategy", 
        "Scenario ID", 
        "Intent", 
        "Fact Score", 
        "Tone Score", 
        "Quality Score", 
        "Overall Score"
    ]

    for file in files:
        path = os.path.join(results_dir, file)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    strategy = data["meta"]["strategy"]
                    for scenario in data["scenarios"]:
                        f_score = scenario["metrics"]["fact_inclusion"]["score"]
                        t_score = scenario["metrics"]["tone_alignment"]["score"]
                        q_score = scenario["metrics"]["professional_quality"]["score"]
                        avg_score = round((f_score + t_score + q_score) / 3, 1)
                        
                        csv_data.append([
                            strategy,
                            scenario["id"],
                            scenario["intent"],
                            f_score,
                            t_score,
                            q_score,
                            avg_score
                        ])
            except Exception as e:
                print(f"Error processing {file}: {e}")
        else:
            print(f"Warning: {file} not found in {results_dir}")

    if csv_data:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(csv_data)
        print(f"Successfully generated {output_file}")
    else:
        print("No data found to export.")

if __name__ == "__main__":
    json_to_csv()
