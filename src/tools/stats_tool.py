import numpy as np
import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from scipy import stats


class StatsToolInput(BaseModel):
    file_path: str = Field(description="Path to the CSV file")


class StatsTool(BaseTool):
    name: str = "StatsTool"
    description: str = "Runs statistical analysis on numeric columns — mean, median, std, skewness, kurtosis, outliers, and correlations."
    args_schema: type[BaseModel] = StatsToolInput

    def _run(self, file_path: str) -> str:
        df = pd.read_csv(file_path)
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            return "No numeric columns found for statistical analysis."

        describe = numeric_df.describe().round(4).to_dict()
        skewness = numeric_df.skew().round(4).to_dict()
        kurt = numeric_df.kurtosis().round(4).to_dict()

        outliers = {}
        for col in numeric_df.columns:
            col_data = numeric_df[col].dropna()
            z_scores = np.abs(stats.zscore(col_data))
            outliers[col] = int((z_scores > 3).sum())

        high_corr_pairs = []
        cols = list(numeric_df.columns)
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                corr_val = numeric_df[cols[i]].corr(numeric_df[cols[j]])
                if abs(corr_val) > 0.7:
                    high_corr_pairs.append({
                        "col1": cols[i],
                        "col2": cols[j],
                        "correlation": round(corr_val, 4),
                    })

        result = {
            "descriptive_stats": describe,
            "skewness": skewness,
            "kurtosis": kurt,
            "outlier_counts_zscore": outliers,
            "high_correlation_pairs": high_corr_pairs,
        }

        return str(result)
