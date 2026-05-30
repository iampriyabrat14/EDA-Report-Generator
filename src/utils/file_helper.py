import uuid
from datetime import datetime
from pathlib import Path


def get_output_dir(subdir: str) -> Path:
    path = Path("outputs") / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_run_id() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:8]


def get_chart_path(filename: str) -> str:
    return str(get_output_dir("charts") / filename)


def get_report_path(run_id: str) -> str:
    return str(get_output_dir("reports") / f"eda_report_{run_id}.html")
