from crewai import Task
from src.agents.statistical_analyst import get_statistical_analyst_agent


def get_stats_task(llm, file_path: str) -> Task:
    agent = get_statistical_analyst_agent(llm)
    return Task(
        description=(
            f"Perform statistical analysis on the numeric columns of the CSV file at {file_path}. "
            "Calculate descriptive statistics (mean, median, std, min, max, quartiles), "
            "skewness, kurtosis, outlier counts using Z-score method, "
            "and identify highly correlated column pairs (correlation > 0.7). "
            "Return all findings in a structured format."
        ),
        expected_output=(
            "A complete statistical analysis report with descriptive stats, skewness, "
            "kurtosis, outlier counts per column, and high correlation pairs."
        ),
        agent=agent,
    )
 