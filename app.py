import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from jinja2 import Environment, FileSystemLoader

from src.crew.eda_crew import run_eda_crew
from src.utils.file_helper import generate_run_id, get_report_path
from src.utils.pdf_helper import html_to_pdf
from src.utils.logger import logger

load_dotenv()

st.set_page_config(
    page_title="EDA Report Generator",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Automated EDA Report Generator")
st.markdown("Upload any CSV file and get a full AI-powered Exploratory Data Analysis report.")
st.divider()

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df_preview = pd.read_csv(uploaded_file)
    uploaded_file.seek(0)

    st.subheader("Dataset Preview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df_preview.shape[0])
    col2.metric("Columns", df_preview.shape[1])
    col3.metric("Duplicate Rows", int(df_preview.duplicated().sum()))

    st.dataframe(df_preview.head(5), use_container_width=True)
    st.divider()

    if st.button("Generate EDA Report", type="primary", use_container_width=True):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        run_id = generate_run_id()

        with st.spinner("AI Agents are analyzing your dataset... This may take a minute."):
            try:
                report_content = run_eda_crew(tmp_path, run_id)

                chart_paths = []
                charts_dir = "outputs/charts"
                if os.path.exists(charts_dir):
                    chart_paths = [
                        os.path.join(charts_dir, f)
                        for f in os.listdir(charts_dir)
                        if run_id in f
                    ]

                env = Environment(loader=FileSystemLoader("templates"))
                template = env.get_template("report_template.html")

                html = template.render(
                    filename=uploaded_file.name,
                    run_id=run_id,
                    generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    rows=df_preview.shape[0],
                    columns=df_preview.shape[1],
                    duplicates=int(df_preview.duplicated().sum()),
                    memory_mb=round(df_preview.memory_usage(deep=True).sum() / 1024 / 1024, 4),
                    report_content=report_content,
                    chart_paths=chart_paths,
                )

                report_path = get_report_path(run_id)
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(html)

                st.success("EDA Report generated successfully!")
                st.divider()

                st.subheader("AI Generated Insights")
                st.markdown(report_content)
                st.divider()

                if chart_paths:
                    st.subheader("Visualizations")
                    cols = st.columns(2)
                    for i, chart in enumerate(chart_paths):
                        cols[i % 2].image(chart, use_container_width=True)
                    st.divider()

                col_html, col_pdf = st.columns(2)

                with open(report_path, "rb") as f:
                    col_html.download_button(
                        label="Download HTML Report",
                        data=f,
                        file_name=f"eda_report_{run_id}.html",
                        mime="text/html",
                        use_container_width=True,
                    )

                try:
                    pdf_path = report_path.replace(".html", ".pdf")
                    with open(report_path, "r", encoding="utf-8") as f:
                        html_to_pdf(f.read(), pdf_path)
                    with open(pdf_path, "rb") as f:
                        col_pdf.download_button(
                            label="Download PDF Report",
                            data=f,
                            file_name=f"eda_report_{run_id}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )
                except Exception as pdf_err:
                    logger.warning(f"PDF generation failed: {pdf_err}")
                    col_pdf.warning("PDF export unavailable.")

            except Exception as e:
                logger.error(f"EDA failed: {e}")
                st.error(f"Something went wrong: {e}")
            finally:
                os.unlink(tmp_path)
