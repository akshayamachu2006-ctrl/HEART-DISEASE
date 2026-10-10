import pandas as pd

# Column names for the Cleveland Heart Disease dataset
columns = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
    "target"
]

# Load dataset
data = pd.read_csv(
   "dataset/heart+disease/heart.csv",
    names=columns,
    na_values="?"
)

print("\n--- FIRST 5 ROWS ---")
print(data.head())

print("\n--- DATASET SHAPE ---")
print(data.shape)

print("\n--- COLUMN NAMES ---")
print(data.columns.tolist())

print("\n--- MISSING VALUES ---")
print(data.isnull().sum())

print("\n--- DATA TYPES ---")
print(data.dtypes)