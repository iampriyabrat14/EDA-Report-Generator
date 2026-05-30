from crewai import Agent
from src.tools.chart_tool import ChartTool


def get_visualization_expert_agent(llm) -> Agent:
    return Agent(
        role="Visualization Expert",
        goal=(
            "Generate insightful charts and visualizations from the dataset including "
            "histograms, boxplots, and correlation heatmaps, and save them to the output directory."
        ),
        backstory=(
            "You are a data visualization specialist who believes that the best insights "
            "come from well-crafted charts. You know exactly which chart type to use "
            "for each type of data and statistical pattern."
        ),
        tools=[ChartTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
