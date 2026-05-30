from crewai import Agent


def get_report_writer_agent(llm) -> Agent:
    return Agent(
        role="Report Writer",
        goal=(
            "Synthesize all findings from the data profiler, statistical analyst, and "
            "visualization expert into a clear, structured, and actionable EDA report "
            "with recommendations for data preprocessing and modeling."
        ),
        backstory=(
            "You are an expert technical writer and data analyst who can translate complex "
            "statistical findings into clear, readable insights. Your reports are known for "
            "being precise, well-structured, and immediately actionable."
        ),
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
