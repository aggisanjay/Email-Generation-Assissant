# 📧 Email Generation Assistant: Strategy Benchmarking

An automated framework for evaluating and comparing Large Language Model (LLM) prompting strategies for professional email generation. This project uses 100% free inference via Groq or Ollama to benchmark an **Advanced Strategy (Strategy A)** against a **Basic Strategy (Strategy B)** using custom evaluation metrics.

## 🚀 Overview

The goal of this project is to determine the impact of advanced prompting techniques (Role-Playing, Few-Shot, and Chain-of-Thought) on the quality of business communications. It features an "LLM-as-a-Judge" pipeline that provides objective scoring across three key dimensions:
1. **Fact Inclusion** (Information Recall)
2. **Tone Alignment** (Context Accuracy)
3. **Professional Quality** (Structure & Grammar)

## 🛠️ Free LLM Setup

### Option A: Groq Cloud (Recommended)
1. Sign up at [Groq Console](https://console.groq.com) (no credit card required).
2. Create an API key.
3. Add to your `.env` file: `GROQ_API_KEY=your_key_here`

### Option B: Ollama (Local)
1. Install [Ollama](https://ollama.com).
2. Pull required models:
   ```bash
   ollama pull llama3.1:8b
   ollama pull llama3.3:70b
   ```
3. Set in `.env`: `LLM_PROVIDER=ollama`

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/email-generation-assistant.git
cd email-generation-assistant

# Setup Virtual Environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Configure Environment
cp .env.example .env
# Edit .env to add your API key or change provider
```

## 📊 Running the Benchmarks

You can run individual evaluations or a full comparative analysis:

```bash
# Run Strategy A (Advanced)
python evaluate.py --strategy a

# Run Strategy B (Basic)
python evaluate.py --strategy b

# Run Comparative Analysis & Generate Summary
python compare.py

# Export Data to CSV (New)
python json_to_csv.py
```

## 📉 Results & Analysis

- **Raw Data**: Found in the `results/` directory as JSON files.
- **CSV Summary**: Available at `results/evaluation_summary.csv` after running the export script.
- **Final Report**: Detailed analysis and prompt templates are available in [final_report.md](final_report.md).

## 🧪 Metric Definitions

| Metric | logic |
| :--- | :--- |
| **Fact Inclusion** | LLM-as-a-Judge audits the email for specific fact recall from the input prompt. |
| **Tone Alignment** | Likert scale (1-5) rating of how well the output matches the requested tone. |
| **Professional Quality** | Composite score of structural completeness, readability (Flesch Ease), and grammar. |

---

Developed for **Advanced Agentic Coding** benchmarking.
