import os
import matplotlib.pyplot as plt
import seaborn as sns

# ensure outputs dir exists
os.makedirs("outputs", exist_ok=True)


def detect_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    plt.figure(figsize=(12, 5))
    sns.boxplot(x=df[col])
    plt.title(f"{col} - Boxplot")
    plt.savefig(os.path.join("outputs", f"outliers_{col}_boxplot.png"))
    plt.close()

    if col != "price" and all(c in df.columns for c in ["price", "quantity_sold"]):
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x=df["price"], y=df["quantity_sold"])
        plt.title("Price vs Quantity Sold")
        plt.savefig(os.path.join("outputs", "scatter_price_quantity.png"))
        plt.close()

    print(f"[{col}] Outliers detected: {outliers.shape[0]}")
    print(f"Lower bound: {lower}")
    print(f"Upper bound: {upper}\n")

    return outliers, lower, upper


def detect_outliers_quantile(df, col, q=0.99):
    threshold = df[col].quantile(q)
    outliers = df[df[col] > threshold]
    print(f"[{col}] Outliers above {q*100}% quantile: {outliers.shape[0]}")
    print(f"Threshold: {threshold}\n")
    return outliers, threshold


def run_outlier_detection(df):

    print("=== OUTLIER DETECTION (IQR) ===")
    for col in ["price", "discount", "quantity_sold"]:
        if col in df.columns:
            detect_outliers_iqr(df, col)

    print("=== OUTLIER DETECTION (QUANTILES) ===")
    for col in ["price", "quantity_sold"]:
        if col in df.columns:
            detect_outliers_quantile(df, col)

    print("Outlier detection completed.\n")
