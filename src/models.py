from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import pickle
import os


def prepare_forecasting_data(df):
    df_model = df.dropna(subset=["quantity_sold"])  # remove missing target
    X = df_model[["price", "discount"]]
    y = df_model["quantity_sold"]

    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test, model_name="model"):
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"{model_name} — MAE: {mae}")
    print(f"{model_name} — RMSE: {rmse}")
    print(f"{model_name} — R²: {r2}\n")

    return mae, rmse, r2


def run_forecasting_model(df, model_output_path="artifacts/rf_model.pkl"):
    print("=== FORECASTING MODEL ===\n")

    X_train, X_test, y_train, y_test = prepare_forecasting_data(df)

    # Linear Regression
    lr_model = train_linear_regression(X_train, y_train)
    evaluate_model(lr_model, X_test, y_test, model_name="linear_regression")

    # Random Forest
    rf_model = train_random_forest(X_train, y_train)
    evaluate_model(rf_model, X_test, y_test, model_name="random_forest")

    # Save RF model
    # Save both models (linear and random forest)
    try:
        out_dir = os.path.dirname(model_output_path)
        if out_dir == "":
            out_dir = "models"
        os.makedirs(out_dir, exist_ok=True)

        rf_path = os.path.join(out_dir, "rf_model.pkl")
        lr_path = os.path.join(out_dir, "lr_model.pkl")

        with open(rf_path, "wb") as f:
            pickle.dump(rf_model, f)

        with open(lr_path, "wb") as f:
            pickle.dump(lr_model, f)
    except Exception:
        pass

    print("Forecasting completed.\n")

    return lr_model, rf_model
