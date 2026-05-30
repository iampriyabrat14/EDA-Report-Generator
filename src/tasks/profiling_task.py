from crewai import Task
from src.agents.data_profiler import get_data_profiler_agent


def get_profiling_task(llm, file_path: str) -> Task:
    agent = get_data_profiler_agent(llm)
    return Task(
        description=(
            f"Load the CSV file from {file_path} and perform a complete data profiling. "
            "Extract the shape, column names, data types, null counts, null percentages, "
            "duplicate row count, memory usage, and a sample of the first 3 rows. "
            "Return a structured summary of all findings."
        ),
        expected_output=(
            "A detailed data profile report including shape, dtypes, null counts, "
            "null percentages, duplicate count, memory usage, and sample rows."
        ),
        agent=agent,
    )
