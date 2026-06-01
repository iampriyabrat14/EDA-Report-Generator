# Changelog

## [1.1.0] - 2026-06-01

### Added
- Categorical column detection in `DataLoaderTool` — auto-identifies object/category columns
- Unique value counts per categorical column in profiling output
- Top-5 value counts for categorical columns in `StatsTool`
- PDF export via `xhtml2pdf` with embedded base64 charts
- Side-by-side HTML + PDF download buttons in Streamlit UI

### Improved
- Chart generation now uses `matplotlib` Agg backend — fixes headless rendering issues
- Suppressed pydantic deprecation warnings in chart tool

---

## [1.0.0] - 2026-05-31

### Initial Release
- Multi-agent CrewAI pipeline with 4 agents: Data Profiler, Statistical Analyst, Visualization Expert, Report Writer
- OpenAI GPT-4o as LLM backbone
- Auto-generates histograms, boxplots, correlation heatmap
- Jinja2 HTML report template with responsive layout
- Streamlit UI with CSV upload, preview, and report download
- CLI entry point via `main.py`
- Unique `run_id` per run — no report overwriting
- Structured logging via Loguru
- 18 unit tests with pytest
