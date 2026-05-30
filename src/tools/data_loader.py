import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class DataLoaderInput(BaseModel):
    file_path: str = Field(description="Path to the CSV file to load")


class DataLoaderTool(BaseTool):
    name: str = "DataLoaderTool"
    description: str = "Loads a CSV file and returns shape, columns, dtypes, null counts, duplicate count, and memory usage."
    args_schema: type[BaseModel] = DataLoaderInput

    def _run(self, file_path: str) -> str:
        df = pd.read_csv(file_path)

        null_counts = df.isnull().sum().to_dict()
        dtype_map = {col: str(dtype) for col, dtype in df.dtypes.items()}
        memory_mb = round(df.memory_usage(deep=True).sum() / 1024 / 1024, 4)

        report = {
            "shape": {"rows": df.shape[0], "columns": df.shape[1]},
            "columns": list(df.columns),
            "dtypes": dtype_map,
            "null_counts": null_counts,
            "null_percentage": {
                col: round(count / df.shape[0] * 100, 2)
                for col, count in null_counts.items()
            },
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_usage_mb": memory_mb,
            "sample_rows": df.head(3).to_dict(orient="records"),
        }

        return str(report)
