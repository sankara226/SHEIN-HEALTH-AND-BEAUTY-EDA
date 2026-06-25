import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style="whitegrid")

# ensure outputs dir exists
os.makedirs("outputs", exist_ok=True)


def eda_distributions(df):
    numeric_cols = ["price", "discount", "quantity_sold"]

    for col in numeric_cols:
        if col not in df.columns:
            continue
        plt.figure(figsize=(12,6))
        sns.histplot(df[col], bins=40, kde=True)
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.savefig(os.path.join("outputs", f"distribution_{col}.png"))
        plt.close()
 

def eda_boxplots(df):
    numeric_cols = ["price", "discount", "quantity_sold"]

    for col in numeric_cols:
        if col not in df.columns:
            continue
        plt.figure(figsize=(12,5))
        sns.boxplot(x=df[col])
        plt.title(f"Boxplot of {col}")
        plt.xlabel(col)
        plt.savefig(os.path.join("outputs", f"boxplot_{col}.png"))
        plt.close()


def eda_relationships(df):
    if all(c in df.columns for c in ["price", "quantity_sold"]):
        plt.figure(figsize=(12,6))
        sns.scatterplot(x="price", y="quantity_sold", data=df, alpha=0.4)
        plt.title("Price vs Quantity Sold")
        plt.savefig(os.path.join("outputs", "price_quantity_sold.png"))
        plt.close()

    if all(c in df.columns for c in ["discount", "quantity_sold"]):
        plt.figure(figsize=(12,6))
        sns.scatterplot(x="discount", y="quantity_sold", data=df, alpha=0.4)
        plt.title("Discount vs Quantity Sold")
        plt.savefig(os.path.join("outputs", "discount_vs_quantity_sold.png"))
        plt.close()

    if all(c in df.columns for c in ["price", "discount", "quantity_sold"]):
        plt.figure(figsize=(12,6))
        corr = df[["price", "discount", "quantity_sold"]].corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title("Correlation matrix")
        plt.savefig(os.path.join("outputs", "correlation_matrix.png"))
        plt.close()


def eda_business_views(df):
    if "price" in df.columns and "quantity_sold" in df.columns:
        df["price_bin"] = pd.cut(df["price"], bins=[0,5,10,20,50,200], include_lowest=True)
        fig, ax = plt.subplots(figsize=(14,8))
        df.groupby("price_bin")["quantity_sold"].mean().plot(kind="bar", ax=ax, color="#4C72B0")
        ax.set_title("Average quantity sold by price range", fontsize=18)
        ax.set_ylabel("Average quantity sold", fontsize=14)
        ax.set_xlabel("Price range", fontsize=14)
        ax.tick_params(axis="x", rotation=45, labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join("outputs", "average_quantity_sold_by_price_range.png"), dpi=150)
        plt.close()

    if "discount" in df.columns and "quantity_sold" in df.columns:
        df["discount_bin"] = pd.cut(df["discount"], bins=[0,0.1,0.2,0.3,0.5,1], include_lowest=True)
        fig, ax = plt.subplots(figsize=(14,8))
        df.groupby("discount_bin")["quantity_sold"].mean().plot(kind="bar", ax=ax, color="#55A868")
        ax.set_title("Average quantity sold by discount range", fontsize=18)
        ax.set_ylabel("Average quantity sold", fontsize=14)
        ax.set_xlabel("Discount range", fontsize=14)
        ax.tick_params(axis="x", rotation=45, labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join("outputs", "average_quantity_sold_by_discount_range.png"), dpi=150)
        plt.close()


def run_full_eda(df):
    eda_distributions(df)
    eda_boxplots(df)
    eda_relationships(df)
    eda_business_views(df)
