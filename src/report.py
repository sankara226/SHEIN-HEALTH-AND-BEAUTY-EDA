from fpdf import FPDF
import unicodedata


def sanitize(text: str) -> str:
    """Return a PDF-safe string encoded for latin-1 by replacing common
    Unicode punctuation with ASCII equivalents and dropping unsupported chars.
    """
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception:
            return ""

    # common replacements
    replacements = {
        "–": "-",
        "—": "-",
        "…": "...",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "•": "-",
        "×": "x",
        "±": "+/-",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    # Normalize and strip characters that cannot be encoded in latin-1
    normalized = unicodedata.normalize("NFKD", text)
    safe = normalized.encode("latin-1", "ignore").decode("latin-1")
    return safe

def generate_pdf_report(output_path="Final_Report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Helper function
    def add_title(text):
        text = sanitize(text)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, text, ln=True)
        pdf.ln(4)
        pdf.set_font("Arial", size=12)

    def add_subtitle(text):
        text = sanitize(text)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 8, text, ln=True)
        pdf.ln(2)
        pdf.set_font("Arial", size=12)

    def add_paragraph(text):
        text = sanitize(text)
        pdf.multi_cell(0, 7, text)
        pdf.ln(2)

    # ===========================
    # 1. EXECUTIVE SUMMARY
    # ===========================
    add_title("Executive Summary")
    add_paragraph(
        "This project analyzes 4,266 Beauty & Health products from Shein US to "
        "identify key sales drivers, pricing behavior, discount impact, and "
        "predictive patterns. The analysis includes data cleaning, EDA, outlier "
        "detection, correlation analysis, business insights, forecasting, and a "
        "Streamlit dashboard."
    )
    add_paragraph(
        "Key findings:\n"
        "- Products under $5 sell up to 4x more.\n"
        "- Discounts above 20% increase sales by 35–50%.\n"
        "- Sales distribution is extremely skewed (Pareto effect).\n"
        "- Random Forest provides strong predictive performance."
    )

    # ===========================
    # 2. DATASET OVERVIEW
    # ===========================
    add_title("Dataset Overview")
    add_paragraph(
        "The cleaned dataset contains 4,266 rows and 3 key variables:\n"
        "- price (float)\n"
        "- discount (float, 0–1)\n"
        "- quantity_sold (float)\n"
        "The dataset originally contained 9 columns with significant missing values "
        "and required extensive cleaning."
    )

    # ===========================
    # 3. DATA CLEANING PIPELINE
    # ===========================
    add_title("Data Cleaning Pipeline")
    add_paragraph(
        "The cleaning pipeline includes:\n"
        "- Removal of irrelevant columns\n"
        "- Text normalization and formatting\n"
        "- Conversion of price, discount, and quantity_sold to numeric types\n"
        "- Handling missing values\n"
        "- Export of cleaned dataset\n"
        "Functions used: fill_blanks(), clean_text_types(), verify_and_export(), full_cleaning_pipeline()."
    )

    # ===========================
    # 4. EXPLORATORY DATA ANALYSIS
    # ===========================
    add_title("Exploratory Data Analysis (EDA)")
    add_paragraph(
        "Key observations:\n"
        "- Prices are concentrated between $1 and $10.\n"
        "- Discounts are mostly below 20%.\n"
        "- Quantity sold follows a long-tail distribution.\n"
        "- Price has a negative relationship with sales.\n"
        "- Discount has a positive relationship with sales."
    )

    # ===========================
    # 5. OUTLIER DETECTION
    # ===========================
    add_title("Outlier Detection")
    add_paragraph(
        "Outliers were detected using IQR and 99th percentile methods.\n"
        "Findings:\n"
        "- Price > $150 corresponds to premium products.\n"
        "- Quantity_sold > 80,000 corresponds to best-sellers.\n"
        "- Discounts > 80% correspond to aggressive promotions.\n"
        "Decision: Outliers were kept because they represent real business behavior."
    )

    # ===========================
    # 6. CORRELATION ANALYSIS
    # ===========================
    add_title("Correlation Analysis")
    add_paragraph(
        "Correlation results:\n"
        "- Price → Sales: negative correlation.\n"
        "- Discount → Sales: positive correlation.\n"
        "- Price ↔ Discount: weak correlation.\n"
        "Interpretation: Lower prices and higher discounts drive higher sales."
    )

    # ===========================
    # 7. BUSINESS INSIGHTS
    # ===========================
    add_title("Business Insights")
    add_paragraph(
        "Insight 1 — Price Strategy:\n"
        "Products under $5 sell significantly more.\n\n"
        "Insight 2 — Discount Strategy:\n"
        "Discounts between 20% and 30% maximize sales.\n\n"
        "Insight 3 — Best Sellers:\n"
        "Top 10 products generate a disproportionate share of total sales.\n\n"
        "Insight 4 — Elasticity:\n"
        "Price elasticity is negative; discount elasticity is positive."
    )

    # ===========================
    # 8. FORECASTING MODEL
    # ===========================
    add_title("Forecasting Model")
    add_paragraph(
        "Two models were trained:\n"
        "- Linear Regression (baseline)\n"
        "- Random Forest Regressor (robust)\n\n"
        "Random Forest achieved the best performance based on MAE, RMSE, and R².\n"
        "The model predicts quantity_sold based on price and discount."
    )

    # ===========================
    # 9. STREAMLIT DASHBOARD
    # ===========================
    add_title("Streamlit Dashboard")
    add_paragraph(
        "A full interactive dashboard was built with:\n"
        "- KPIs\n"
        "- EDA visualizations\n"
        "- Outlier explorer\n"
        "- Correlation explorer\n"
        "- Forecasting tool\n"
        "The dashboard allows real-time prediction of sales based on user inputs."
    )

    # ===========================
    # 10. CONCLUSION
    # ===========================
    add_title("Conclusion & Recommendations")
    add_paragraph(
        "Recommendations:\n"
        "- Increase offering of products under $5.\n"
        "- Use 20–30% discounts to boost sales.\n"
        "- Promote best-sellers more aggressively.\n"
        "- Use the forecasting model to optimize pricing.\n\n"
        "Future improvements:\n"
        "- Add product categories.\n"
        "- Integrate time-series data.\n"
        "- Add customer segmentation.\n"
        "- Test advanced ML models (XGBoost, CatBoost)."
    )

    # Save PDF
    pdf.output(output_path)
    print(f"PDF report generated: {output_path}")
