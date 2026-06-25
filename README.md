# SHEIN Beauty & Health — EDA, Modeling & Dashboard

## Introduction

This repository refactors a monolithic analysis script for Shein US Beauty & Health
products into a professional, modular project. The goal is to provide a reproducible
pipeline for data cleaning, exploratory data analysis (EDA), outlier detection,
correlation analysis, business insights extraction, predictive modeling (Linear
Regression and Random Forest), PDF report generation and an interactive Streamlit
dashboard.

## Project structure

```
├── data/                      # place raw datasets here
├── artifacts/                 # saved models and binary artifacts (lr_model.pkl, rf_model.pkl)
├── outputs/                   # exported charts and reports
├── src/                       # modular source code
│   ├── __init__.py
│   ├── data_pipeline.py
│   ├── eda.py
│   ├── outliers.py
│   ├── correlation.py
│   ├── insights.py
│   ├── models.py
│   ├── dashboard.py
│   └── report.py
├── main.py                    # orchestrator (clean → EDA → models → report)
├── app.py                     # streamlit entrypoint
├── requirements.txt
└── README.md
```

## Pipeline and technical details

- `src/data_pipeline.py`: loading, basic exploration, missing-value imputation,
	text normalization, type conversion and export of `cleaned_dataset.csv`.
- `src/eda.py`: distribution plots, boxplots, relationships and business view charts.
- `src/outliers.py`: IQR and percentile-based outlier detection and visualization.
- `src/correlation.py`: scatterplots and correlation heatmap exports.
- `src/insights.py`: business-focused analyses (top/bottom sellers, elasticity).
- `src/models.py`: data preparation, training of Linear Regression and Random
	Forest models, evaluation metrics (MAE, RMSE, R²) and saving of both models to
	the `artifacts/` directory as `lr_model.pkl` and `rf_model.pkl`.
- `src/dashboard.py`: Streamlit dashboard to explore KPIs, EDA plots and perform
	on-demand predictions using the Random Forest model.
- `src/report.py`: PDF report generator (FPDF) summarizing findings and
	recommendations.

Modeling choices

- Random Forest is used as the main predictive model because it handles
	non-linear relationships and is robust to outliers.
- Linear Regression is kept as a simple baseline for interpretability.

## Key business insights (from the analysis)

- Products priced below $5 demonstrate significantly higher sales volumes.
- Discounts in the 20–30% range appear to maximize quantity sold.
- Sales are heavily skewed: a small number of best-sellers account for a large
	share of total sales.

Recommendations

- Expand the low-price product assortment.
- Run targeted promotions at ~20–30% discount for volume uplift.
- Promote best-sellers and use the forecasting model to optimize pricing.

## Quick start

1. Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Place the raw CSV file in `data/` or provide its path and run the pipeline:

```bash
python main.py --path /path/to/us-shein-beauty_and_health-4267.csv
```

3. Start the Streamlit dashboard (after the pipeline has produced
	 `cleaned_dataset.csv` and trained models):

```bash
streamlit run app.py
```

4. Output files (charts, report) will be saved under `outputs/`. Trained models
	are saved to `artifacts/` as `lr_model.pkl` and `rf_model.pkl`.



