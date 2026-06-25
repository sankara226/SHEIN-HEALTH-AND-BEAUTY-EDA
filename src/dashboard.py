import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

sns.set(style="whitegrid")


@st.cache_data
def load_data(path="data/cleaned_dataset.csv"):
    return pd.read_csv(path)


def load_model(path="artifacts/rf_model.pkl"):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception:
        return None


def run_dashboard():
    data_path = "data/cleaned_dataset.csv"
    model_path = "artifacts/rf_model.pkl"

    # Lightweight pre-flight checks
    if not os.path.exists(data_path):
        st.sidebar.error("Cleaned dataset not found: data/cleaned_dataset.csv")
        st.sidebar.info("Run the full pipeline to generate it: `python main.py --path <raw_csv_path>`")
        st.title("Beauty & Health Sales Dashboard")
        st.write("Waiting for `data/cleaned_dataset.csv` to be generated.\n\nRun `python main.py --path /path/to/raw.csv` to create it.")
        return

    df = load_data(data_path)
    rf_model = load_model(model_path)

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Overview", "EDA", "Forecasting"])

    if page == "Overview":
        st.title("Beauty & Health Sales Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Products", df.shape[0])
        col2.metric("Average Price", round(df["price"].mean(), 2))
        col3.metric("Average Discount", f"{round(df['discount'].mean()*100, 1)}%")

        st.subheader("Distribution of Quantity Sold")
        fig, ax = plt.subplots(figsize=(12,6))
        sns.histplot(df["quantity_sold"], bins=40, kde=True, ax=ax)
        st.pyplot(fig)

    if page == "EDA":
        st.title("Exploratory Data Analysis")

        st.subheader("Price vs Quantity Sold")
        fig, ax = plt.subplots(figsize=(12,6))
        sns.scatterplot(x=df["price"], y=df["quantity_sold"], alpha=0.4, ax=ax)
        st.pyplot(fig)

        st.subheader("Discount vs Quantity Sold")
        fig, ax = plt.subplots(figsize=(12,6))
        sns.scatterplot(x=df["discount"], y=df["quantity_sold"], alpha=0.4, ax=ax)
        st.pyplot(fig)

        st.subheader("Correlation Matrix")
        fig, ax = plt.subplots(figsize=(12,6))
        sns.heatmap(df[["price","discount","quantity_sold"]].corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    if page == "Forecasting":
        st.title("Sales Forecasting Tool")

        price = st.number_input("Price ($)", min_value=0.1, max_value=300.0, value=10.0)
        discount = st.slider("Discount (%)", 0, 90, 10)

        if st.button("Predict Sales"):
            if rf_model is None:
                st.warning("Model not found. Train models first (run main.py). Predictions disabled.")
            else:
                pred = rf_model.predict([[price, discount/100]])[0]
                st.success(f"Predicted Quantity Sold: {int(pred)} units")


if __name__ == "__main__":
    run_dashboard()
