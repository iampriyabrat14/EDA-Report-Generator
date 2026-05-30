import os
from crewai import Crew, Process, LLM

from src.tasks.profiling_task import get_profiling_task
from src.tasks.stats_task import get_stats_task
from src.tasks.visualization_task import get_visualization_task
from src.tasks.report_task import get_report_task
from src.utils.logger import logger


def build_eda_crew(file_path: str, run_id: str) -> Crew:
    llm = LLM(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

    profiling_task = get_profiling_task(llm, file_path)
    stats_task = get_stats_task(llm, file_path)
    visualization_task = get_visualization_task(llm, file_path, run_id)
    report_task = get_report_task(llm, file_path)

    logger.info(f"Building EDA Crew for run_id: {run_id}")

    return Crew(
        agents=[
            profiling_task.agent,
            stats_task.agent,
            visualization_task.agent,
            report_task.agent,
        ],
        tasks=[
            profiling_task,
            stats_task,
            visualization_task,
            report_task,
        ],
        process=Process.sequential,
        verbose=True,
    )


def run_eda_crew(file_path: str, run_id: str) -> str:
    crew = build_eda_crew(file_path, run_id)
    logger.info(f"Starting EDA Crew for file: {file_path}")
    result = crew.kickoff()
    logger.info(f"EDA Crew completed for run_id: {run_id}")
    return str(result)
