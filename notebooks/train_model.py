import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping


# --------------------------------------------------
# 1. Column names
# --------------------------------------------------

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


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

data_path = "dataset/heart+disease/heart.csv"

data = pd.read_csv(
    data_path,
    names=columns,
    na_values="?"
)

print("\nDataset loaded successfully!")
print("Original shape:", data.shape)


# --------------------------------------------------
# 3. Convert columns to numeric
# --------------------------------------------------

for column in columns:
    data[column] = pd.to_numeric(data[column], errors="coerce")


# --------------------------------------------------
# 4. Handle missing values
# --------------------------------------------------

X = data.drop("target", axis=1)
y = data["target"]

imputer = SimpleImputer(strategy="median")
X = imputer.fit_transform(X)


# --------------------------------------------------
# 5. Convert target into binary classification
# --------------------------------------------------

# 0 = No heart disease
# 1,2,3,4 = Heart disease

y = (y > 0).astype(int)

print("\nTarget distribution:")
print(y.value_counts())


# --------------------------------------------------
# 6. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


# --------------------------------------------------
# 7. Feature scaling
# --------------------------------------------------

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# --------------------------------------------------
# 8. Build ANN model
# --------------------------------------------------

model = Sequential([
    Dense(32, activation="relu", input_shape=(13,)),
    Dropout(0.2),

    Dense(16, activation="relu"),
    Dropout(0.2),

    Dense(8, activation="relu"),

    Dense(1, activation="sigmoid")
])


# --------------------------------------------------
# 9. Compile model
# --------------------------------------------------

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


# --------------------------------------------------
# 10. Display model architecture
# --------------------------------------------------

print("\nANN Architecture:")
model.summary()


# --------------------------------------------------
# 11. Early stopping
# --------------------------------------------------

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True
)


# --------------------------------------------------
# 12. Train ANN
# --------------------------------------------------

print("\nTraining ANN...")

history = model.fit(
    X_train,
    y_train,
    validation_split=0.20,
    epochs=100,
    batch_size=16,
    callbacks=[early_stopping],
    verbose=1
)


# --------------------------------------------------
# 13. Evaluate model
# --------------------------------------------------

y_probability = model.predict(X_test)

y_pred = (y_probability >= 0.5).astype(int).ravel()

accuracy = accuracy_score(y_test, y_pred)

print("\n--------------------------------")
print("MODEL EVALUATION")
print("--------------------------------")

print(f"Test Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------------------------
# 14. Create model directory
# --------------------------------------------------

os.makedirs("model", exist_ok=True)


# --------------------------------------------------
# 15. Save trained ANN model
# --------------------------------------------------

model.save("model/heart_disease_ann.keras")

print("\nANN model saved successfully!")


# --------------------------------------------------
# 16. Save scaler and imputer
# --------------------------------------------------

joblib.dump(
    scaler,
    "model/scaler.pkl"
)

joblib.dump(
    imputer,
    "model/imputer.pkl"
)

print("Scaler saved successfully!")
print("Imputer saved successfully!")


# --------------------------------------------------
# 17. Save training history
# --------------------------------------------------

history_df = pd.DataFrame(history.history)

history_df.to_csv(
    "model/training_history.csv",
    index=False
)

print("Training history saved successfully!")

print("\nPROJECT TRAINING COMPLETED! 🎉")