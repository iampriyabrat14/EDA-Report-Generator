# EDA Report Generator 🤖

An AI-powered Automated Exploratory Data Analysis (EDA) tool built with **CrewAI** multi-agent framework. Upload any CSV file and get a full EDA report with statistics, visualizations, and AI-generated insights — exportable as **HTML or PDF**.

---

## Features

- Multi-agent pipeline (Data Profiler → Statistical Analyst → Visualization Expert → Report Writer)
- Auto-generates charts: histograms, boxplots, correlation heatmap
- Detects nulls, duplicates, outliers, and high correlations
- Exports a clean **HTML report** per run
- Exports a **PDF report** with embedded charts
- Streamlit UI for easy file upload and report download
- CLI support for terminal usage

---

## Visual Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INPUT                                   │
│                  Upload CSV  (Streamlit UI / CLI)                   │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CrewAI Orchestrator                            │
│                  Sequential Multi-Agent Pipeline                    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
          ┌─────────────────▼─────────────────┐
          │         Agent 1                   │
          │       Data Profiler               │
          │  ─────────────────────────────    │
          │  Tool  : DataLoaderTool           │
          │  Output: Shape, Dtypes, Nulls,    │
          │          Duplicates, Memory       │
          └─────────────────┬─────────────────┘
                            │
          ┌─────────────────▼─────────────────┐
          │         Agent 2                   │
          │    Statistical Analyst            │
          │  ─────────────────────────────    │
          │  Tool  : StatsTool                │
          │  Output: Mean, Std, Skewness,     │
          │          Outliers, Correlations   │
          └─────────────────┬─────────────────┘
                            │
          ┌─────────────────▼─────────────────┐
          │         Agent 3                   │
          │    Visualization Expert           │
          │  ─────────────────────────────    │
          │  Tool  : ChartTool                │
          │  Output: Histograms, Boxplots,    │
          │          Correlation Heatmap      │
          └─────────────────┬─────────────────┘
                            │
          ┌─────────────────▼─────────────────┐
          │         Agent 4                   │
          │       Report Writer               │
          │  ─────────────────────────────    │
          │  Tool  : GPT-4o (LLM only)        │
          │  Output: Full EDA Report          │
          │          in Markdown              │
          └─────────────────┬─────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌───────────────────┐           ┌───────────────────┐
│   HTML Report     │           │   PDF Report      │
│  (Jinja2 Template)│           │  (xhtml2pdf)      │
│  outputs/reports/ │           │  outputs/reports/ │
└───────────────────┘           └───────────────────┘
            │                               │
            └───────────────┬───────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Streamlit Dashboard                             │
│        AI Insights  │  Charts Grid  │  Download HTML / PDF         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | CrewAI |
| LLM | OpenAI GPT-4o |
| Data Processing | Pandas, NumPy, SciPy |
| Visualization | Matplotlib, Seaborn |
| Report (HTML) | Jinja2 HTML Template |
| Report (PDF) | xhtml2pdf |
| UI | Streamlit |
| Logging | Loguru |

---

## Project Structure

```
EDA-Report-Generator/
├── src/
│   ├── agents/
│   │   ├── data_profiler.py
│   │   ├── statistical_analyst.py
│   │   ├── visualization_expert.py
│   │   └── report_writer.py
│   ├── tasks/
│   │   ├── profiling_task.py
│   │   ├── stats_task.py
│   │   ├── visualization_task.py
│   │   └── report_task.py
│   ├── tools/
│   │   ├── data_loader.py
│   │   ├── stats_tool.py
│   │   └── chart_tool.py
│   ├── crew/
│   │   └── eda_crew.py
│   ├── config/
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   └── utils/
│       ├── logger.py
│       ├── file_helper.py
│       └── pdf_helper.py
├── templates/
│   └── report_template.html
├── outputs/
│   ├── charts/          ← Generated charts per run
│   └── reports/         ← Final HTML & PDF reports
├── sample_data/
│   └── sample.csv
├── tests/
│   ├── test_tools.py
│   └── test_crew.py
├── app.py               ← Streamlit UI
├── main.py              ← CLI entry point
└── requirements.txt
```

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/iampriyabrat14/EDA-Report-Generator.git
cd EDA-Report-Generator
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Add your OpenAI API key in .env
```

---

## Usage

### Run via Streamlit UI
```bash
streamlit run app.py
```

### Run via CLI
```bash
python main.py --file sample_data/sample.csv
```

### Run Tests
```bash
pytest tests/ -v
```

---

## Agents

| Agent | Role | Tool Used |
|---|---|---|
| Data Profiler | Shape, dtypes, nulls, duplicates, memory | DataLoaderTool |
| Statistical Analyst | Mean, std, skewness, outliers, correlations | StatsTool |
| Visualization Expert | Generates & saves charts | ChartTool |
| Report Writer | Synthesizes all findings into final report | None (LLM only) |

---

## Output

Each run generates a unique `run_id` (e.g. `20260531_143022_abc12345`) and produces:

```
outputs/
├── charts/
│   ├── hist_age_<run_id>.png
│   ├── box_salary_<run_id>.png
│   └── heatmap_<run_id>.png
└── reports/
    ├── eda_report_<run_id>.html
    └── eda_report_<run_id>.pdf
```

---

## Sample Dataset

A built-in `sample_data/sample.csv` is included with 40 rows covering:
`age`, `salary`, `experience_years`, `department`, `gender`, `performance_score`, `is_promoted`

---

## Author

**Priyabrat Dalbehera**  
Senior Software Engineer — GenAI & AI Systems  
[GitHub](https://github.com/iampriyabrat14) | [LinkedIn](https://www.linkedin.com/in/priyabrat-dalbehera-p521/)
