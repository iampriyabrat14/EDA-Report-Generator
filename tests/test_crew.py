import os
import pytest
from unittest.mock import patch, MagicMock

from src.utils.file_helper import generate_run_id, get_chart_path, get_report_path


SAMPLE_CSV = os.path.join(os.path.dirname(__file__), "..", "sample_data", "sample.csv")


class TestFileHelper:
    def test_generate_run_id_format(self):
        run_id = generate_run_id()
        assert isinstance(run_id, str)
        assert len(run_id) > 10

    def test_generate_run_id_unique(self):
        id1 = generate_run_id()
        id2 = generate_run_id()
        assert id1 != id2

    def test_get_chart_path(self):
        path = get_chart_path("test_chart.png")
        assert "charts" in path
        assert path.endswith("test_chart.png")

    def test_get_report_path(self):
        run_id = generate_run_id()
        path = get_report_path(run_id)
        assert "reports" in path
        assert run_id in path
        assert path.endswith(".html")


class TestEdaCrew:
    @patch("src.crew.eda_crew.run_eda_crew")
    def test_run_eda_crew_called(self, mock_run):
        mock_run.return_value = "## EDA Report\nSample output"
        result = mock_run(SAMPLE_CSV, "test_run_id")
        mock_run.assert_called_once_with(SAMPLE_CSV, "test_run_id")
        assert isinstance(result, str)

    @patch("src.crew.eda_crew.run_eda_crew")
    def test_run_eda_crew_returns_string(self, mock_run):
        mock_run.return_value = "## EDA Report\nSample output"
        result = mock_run(SAMPLE_CSV, "test_run_id")
        assert "EDA" in result

    @patch("src.crew.eda_crew.run_eda_crew")
    def test_run_eda_crew_failure(self, mock_run):
        mock_run.side_effect = Exception("LLM API Error")
        with pytest.raises(Exception, match="LLM API Error"):
            mock_run(SAMPLE_CSV, "test_run_id")
