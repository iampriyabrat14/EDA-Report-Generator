import argparse
import os
import pandas as pd
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

from src.crew.eda_crew import run_eda_crew
from src.utils.file_helper import generate_run_id, get_report_path, get_chart_path
from src.utils.logger import logger

load_dotenv()


def render_report(file_path: str, run_id: str, report_content: str, chart_paths: list) -> str:
    df = pd.read_csv(file_path)

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")

    html = template.render(
        filename=os.path.basename(file_path),
        run_id=run_id,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        rows=df.shape[0],
        columns=df.shape[1],
        duplicates=int(df.duplicated().sum()),
        memory_mb=round(df.memory_usage(deep=True).sum() / 1024 / 1024, 4),
        report_content=report_content,
        chart_paths=chart_paths,
    )

    report_path = get_report_path(run_id)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    return report_path


def main():
    parser = argparse.ArgumentParser(description="Automated EDA Report Generator")
    parser.add_argument("--file", required=True, help="Path to the CSV file")
    args = parser.parse_args()

    file_path = args.file

    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    run_id = generate_run_id()
    logger.info(f"Starting EDA for: {file_path} | run_id: {run_id}")

    report_content = run_eda_crew(file_path, run_id)

    chart_paths = []
    charts_dir = "outputs/charts"
    if os.path.exists(charts_dir):
        chart_paths = [
            os.path.join(charts_dir, f)
            for f in os.listdir(charts_dir)
            if run_id in f
        ]

    report_path = render_report(file_path, run_id, report_content, chart_paths)
    logger.info(f"Report saved: {report_path}")
    print(f"\nReport generated: {report_path}")


if __name__ == "__main__":
    main()
