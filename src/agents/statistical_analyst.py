from crewai import Agent
from src.tools.stats_tool import StatsTool


def get_statistical_analyst_agent(llm) -> Agent:
    return Agent(
        role="Statistical Analyst",
        goal=(
            "Perform deep statistical analysis on numeric columns of the dataset including "
            "descriptive statistics, skewness, kurtosis, outlier detection, and correlation analysis."
        ),
        backstory=(
            "You are a senior statistician and data scientist who specializes in uncovering "
            "hidden patterns in data. You are highly skilled at interpreting distributions, "
            "identifying anomalies, and finding relationships between variables."
        ),
        tools=[StatsTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
