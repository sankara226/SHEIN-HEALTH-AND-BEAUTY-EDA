import pandas as pd

# STEP 1: FILE IMPORT AND CLEANING (modularized)

head = "="*60


def explore_data(df):
    head = "="*60
    space = ""
    missing_values = df.isna().sum()
    missing_values_percentage = (df.isna().sum()/len(df))*100
    characteristics = [{
          "head": head,
          "name": "SIZE",
          "value": df.size,
          "feet": head,
          "space": space
      }, {
          "head": head,
          "name": "SHAPE",
          "value": df.shape,
          "feet": head,
          "space": space
      }, {
          "head": head,
          "name": "INFO",
          "value": df.info(),
          "feet": head,
          "space": space
          }, {
          "head": head,
          "name": "DESCRIBE",
          "value": df.describe(),
          "feet": head,
          "space": space
          }, {
          "head": head,
          "name": "DATAFRAME HEAD",
          "value": df.head(),
          "feet": head,
          "space": space
          }, {
          "head": head,
          "name": "DATAFRAME TAIL",
          "value": df.tail(),
          "feet": head,
          "space": space
          }, {
          "head": head,
          "name": "COLUMNS",
          "value": df.columns,
          "feet": head,
          "space": space
          }, {
          "head": head,
          "name": "DATA TYPES",
          "value": df.dtypes,
          "feet": head,
          "space": space
          }, {
          "head": head,
          "name": "MISSING VALUES",
          "value": missing_values.sort_values(ascending=False),
          "feet": head,
          "space": space
          }, {
          "head": head,
          "name": "MISSING VALUES PERCENTAGE",
          "value": missing_values_percentage.sort_values(ascending=False),
          "feet": head,
          "space": space
      }]
    for characteristic in characteristics:
      print(characteristic["head"])
      print(characteristic["name"])
      print(characteristic["value"])
      print(characteristic["feet"])
      print(characteristic["space"])

    return None


def fill_blanks(df):
  df = df.drop(columns=["goods-title-link--jump", "goods-title-link--jump href", "goods-title-link", "color-count", "rank-title", "rank-sub"], errors='ignore')
  df = df.rename(columns={"selling_proposition": "quantity_sold"})
  if "discount" in df.columns:
      df["discount"] = df["discount"].fillna(df["discount"].mode()[0])
  if "quantity_sold" in df.columns:
      df["quantity_sold"] = df["quantity_sold"].fillna(df["quantity_sold"].mode()[0])
  
  return df


def clean_text_types(df):
  df = df.apply(lambda col: col.str.lower() if col.dtype == "object" else col)

  # price cleanup
  if "price" in df.columns:
      df["price"] = df["price"].astype(str).str.replace("$", "", regex=False)
  # discount cleanup
  if "discount" in df.columns:
      df["discount"] = df["discount"].astype(str).str.strip().str.replace("%", "", regex=False)
      df["discount"] = df["discount"].str.strip().str.replace("-", "", regex=False)
      df["discount"] = df["discount"].str.replace("off", "", regex=False)

  # quantity_sold cleanup
  if "quantity_sold" in df.columns:
      q = df["quantity_sold"].astype(str)
      q = q.str.strip().str.replace("k", "000", regex=False)
      q = q.str.replace("+", "", regex=False)
      q = q.str.replace(".", "", regex=False)
      q = q.str.replace("recently", "", regex=False)
      q = q.str.replace("sold", "", regex=False)
      q = q.str.replace(",", "", regex=False)
      df["quantity_sold"] = q

  # Convert types when possible
  try:
      if "quantity_sold" in df.columns:
          df["quantity_sold"] = df["quantity_sold"].replace(["", None], 0)
          df["quantity_sold"] = df["quantity_sold"].astype(float)
  except Exception:
      pass

  try:
      if "discount" in df.columns:
          df["discount"] = df["discount"].astype(float)
          df["discount"] = df["discount"]/100
  except Exception:
      pass

  try:
      if "price" in df.columns:
          df["price"] = df["price"].astype(float)
  except Exception:
      pass
  
  return df 


def verify_and_export(df, export_path="data/cleaned_dataset.csv"):
    print("FINAL SHAPE:", df.shape)
    print("FINAL DATA TYPES:")
    print(df.dtypes)
    print("")
    print("MISSING VALUES AFTER CLEANING:")
    print(df.isna().sum())
    print("")

    # Ensure data directory exists and export
    import os
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    df.to_csv(export_path, index=False)
    print(f"Dataset successfully exported to: {export_path}")

    return df


def full_cleaning_pipeline(path):

    df = pd.read_csv(path)
    print("File loaded successfully.")
    explore_data(df)

    df = fill_blanks(df)
    print("Blanks filled.")
    explore_data(df)

    df = clean_text_types(df)
    print("Text cleaned and types corrected.")
    explore_data(df)

    df = verify_and_export(df)

    print("="*60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("="*60)

    return df


@pd.api.extensions.register_dataframe_accessor("pipeline")
class _DummyAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def run_full_pipeline(self, path):
        return full_cleaning_pipeline(path)
