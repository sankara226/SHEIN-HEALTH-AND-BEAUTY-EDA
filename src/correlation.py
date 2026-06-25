import os
import matplotlib.pyplot as plt
import seaborn as sns

# ensure outputs dir exists
os.makedirs("outputs", exist_ok=True)


def correlation_scatterplots(df):

    if all(c in df.columns for c in ["price", "quantity_sold"]):
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x=df["price"], y=df["quantity_sold"], alpha=0.4)
        plt.title("Price vs Quantity Sold")
        plt.savefig(os.path.join("outputs", "scatter_price_quantity.png"))
        plt.close()

    if all(c in df.columns for c in ["discount", "quantity_sold"]):
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x=df["discount"], y=df["quantity_sold"], alpha=0.4)
        plt.title("Discount vs Quantity Sold")
        plt.savefig(os.path.join("outputs", "scatter_discount_quantity.png"))
        plt.close()

    if all(c in df.columns for c in ["price", "discount"]):
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x=df["price"], y=df["discount"], alpha=0.4)
        plt.title("Price vs Discount")
        plt.savefig(os.path.join("outputs", "scatter_price_discount.png"))
        plt.close()

    print("Scatterplots saved.\n")


def run_correlation_analysis(df):
    correlation_scatterplots(df)

    print("Correlation analysis completed.\n")
