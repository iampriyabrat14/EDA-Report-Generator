import os
import pytest
import pandas as pd

from src.tools.data_loader import DataLoaderTool
from src.tools.stats_tool import StatsTool

SAMPLE_CSV = os.path.join(os.path.dirname(__file__), "..", "sample_data", "sample.csv")


@pytest.fixture
def sample_path():
    return SAMPLE_CSV


class TestDataLoaderTool:
    def test_returns_string(self, sample_path):
        tool = DataLoaderTool()
        result = tool._run(file_path=sample_path)
        assert isinstance(result, str)

    def test_contains_shape(self, sample_path):
        tool = DataLoaderTool()
        result = tool._run(file_path=sample_path)
        assert "shape" in result

    def test_contains_columns(self, sample_path):
        tool = DataLoaderTool()
        result = tool._run(file_path=sample_path)
        assert "columns" in result

    def test_contains_null_counts(self, sample_path):
        tool = DataLoaderTool()
        result = tool._run(file_path=sample_path)
        assert "null_counts" in result

    def test_contains_duplicate_rows(self, sample_path):
        tool = DataLoaderTool()
        result = tool._run(file_path=sample_path)
        assert "duplicate_rows" in result

    def test_file_not_found(self):
        tool = DataLoaderTool()
        with pytest.raises(Exception):
            tool._run(file_path="nonexistent.csv")


class TestStatsTool:
    def test_returns_string(self, sample_path):
        tool = StatsTool()
        result = tool._run(file_path=sample_path)
        assert isinstance(result, str)

    def test_contains_descriptive_stats(self, sample_path):
        tool = StatsTool()
        result = tool._run(file_path=sample_path)
        assert "descriptive_stats" in result

    def test_contains_skewness(self, sample_path):
        tool = StatsTool()
        result = tool._run(file_path=sample_path)
        assert "skewness" in result

    def test_contains_outliers(self, sample_path):
        tool = StatsTool()
        result = tool._run(file_path=sample_path)
        assert "outlier_counts_zscore" in result

    def test_contains_high_correlation(self, sample_path):
        tool = StatsTool()
        result = tool._run(file_path=sample_path)
        assert "high_correlation_pairs" in result
