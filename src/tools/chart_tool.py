import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.utils.file_helper import get_chart_path


class ChartToolInput(BaseModel):
    file_path: str = Field(description="Path to the CSV file")
    run_id: str = Field(description="Unique run ID for naming chart files")


class ChartTool(BaseTool):
    name: str = "ChartTool"
    description: str = "Generates and saves EDA charts — histograms, boxplots, and correlation heatmap."
    args_schema: type[BaseModel] = ChartToolInput

    def _run(self, file_path: str, run_id: str) -> str:
        df = pd.read_csv(file_path)
        numeric_df = df.select_dtypes(include=[np.number])
        saved_charts = []

        if numeric_df.empty:
            return "No numeric columns found to generate charts."

        # Histograms
        for col in numeric_df.columns:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.hist(numeric_df[col].dropna(), bins=30, color="#4C72B0", edgecolor="white")
            ax.set_title(f"Distribution of {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Frequency")
            path = get_chart_path(f"hist_{col}_{run_id}.png")
            fig.savefig(path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            saved_charts.append(path)

        # Boxplots
        for col in numeric_df.columns:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.boxplot(numeric_df[col].dropna(), patch_artist=True,
                       boxprops=dict(facecolor="#4C72B0", color="#4C72B0"),
                       medianprops=dict(color="white"))
            ax.set_title(f"Boxplot of {col}")
            ax.set_ylabel(col)
            path = get_chart_path(f"box_{col}_{run_id}.png")
            fig.savefig(path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            saved_charts.append(path)

        # Correlation Heatmap
        if len(numeric_df.columns) > 1:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(
                numeric_df.corr(),
                annot=True,
                fmt=".2f",
                cmap="coolwarm",
                ax=ax,
                linewidths=0.5,
            )
            ax.set_title("Correlation Heatmap")
            path = get_chart_path(f"heatmap_{run_id}.png")
            fig.savefig(path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            saved_charts.append(path)

        return str({"saved_charts": saved_charts})
