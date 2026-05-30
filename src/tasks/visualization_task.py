from crewai import Task
from src.agents.visualization_expert import get_visualization_expert_agent


def get_visualization_task(llm, file_path: str, run_id: str) -> Task:
    agent = get_visualization_expert_agent(llm)
    return Task(
        description=(
            f"Generate EDA charts for the CSV file at {file_path} using run_id {run_id}. "
            "Create histograms and boxplots for each numeric column. "
            "Create a correlation heatmap for all numeric columns. "
            "Save all charts to the outputs/charts/ directory. "
            "Return the list of saved chart file paths."
        ),
        expected_output=(
            "A list of file paths for all saved charts including histograms, "
            "boxplots, and the correlation heatmap."
        ),
        agent=agent,
    )
