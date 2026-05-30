from crewai import Task
from src.agents.report_writer import get_report_writer_agent


def get_report_task(llm, file_path: str) -> Task:
    agent = get_report_writer_agent(llm)
    return Task(
        description=(
            f"Using the outputs from the data profiler, statistical analyst, and visualization expert, "
            f"write a comprehensive EDA report for the dataset at {file_path}. "
            "The report must include:\n"
            "- Dataset overview (shape, columns, memory)\n"
            "- Data quality summary (nulls, duplicates)\n"
            "- Statistical insights (distributions, skewness, outliers)\n"
            "- Correlation findings\n"
            "- List of generated charts\n"
            "- Recommendations for data preprocessing and next steps\n"
            "Return the full report as a well-structured markdown text."
        ),
        expected_output=(
            "A complete, well-structured EDA report in markdown format covering "
            "dataset overview, data quality, statistical insights, correlations, "
            "chart references, and preprocessing recommendations."
        ),
        agent=agent,
    )
