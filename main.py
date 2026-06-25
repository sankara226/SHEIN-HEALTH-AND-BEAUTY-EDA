"""
Orchestrator script to run the full pipeline: cleaning, EDA, outliers,
correlation, business insights, modeling and report generation.

Usage: python main.py --path <path_to_raw_csv>
"""
import os
from src import data_pipeline
from src import eda
from src import outliers
from src import correlation
from src import insights
from src import models
from src import report


def ensure_dirs():
    for d in ["data", "artifacts", "outputs"]:
        os.makedirs(d, exist_ok=True)


def run_all(path):
    ensure_dirs()

    # 1) Cleaning
    cleaned_df = data_pipeline.full_cleaning_pipeline(path)

    # 2) EDA
    eda.run_full_eda(cleaned_df)

    # 3) Outliers
    outliers.run_outlier_detection(cleaned_df)

    # 4) Correlation
    correlation.run_correlation_analysis(cleaned_df)

    # 5) Business Insights
    insights.run_business_insights(cleaned_df)

    # 6) Forecasting & save models
    lr, rf = models.run_forecasting_model(cleaned_df, model_output_path="artifacts/rf_model.pkl")

    # 7) Report
    report.generate_pdf_report("outputs/Final_Report.pdf")

    print("All tasks completed. Models/artifacts are in /artifacts and visual outputs in /outputs directories.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="/content/us-shein-beauty_and_health-4267.csv", help="Path to raw CSV file")
    args = parser.parse_args()

    run_all(args.path)
