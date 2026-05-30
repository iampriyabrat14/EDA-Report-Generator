from crewai import Agent
from src.tools.data_loader import DataLoaderTool


def get_data_profiler_agent(llm) -> Agent:
    return Agent(
        role="Data Profiler",
        goal=(
            "Analyze the structure of the uploaded CSV dataset and extract key metadata "
            "including shape, data types, null values, duplicates, and memory usage."
        ),
        backstory=(
            "You are an expert data engineer with years of experience profiling raw datasets. "
            "You have a sharp eye for data quality issues and can quickly identify structural "
            "problems in any dataset."
        ),
        tools=[DataLoaderTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
