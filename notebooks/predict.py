import numpy as np
import joblib
from tensorflow.keras.models import load_model


# Load trained model
model = load_model("model/heart_disease_ann.keras")

# Load preprocessing objects
scaler = joblib.load("model/scaler.pkl")
imputer = joblib.load("model/imputer.pkl")


# --------------------------------------------------
# Patient information
# --------------------------------------------------

patient = np.array([[
    63,     # age
    1,      # sex
    1,      # chest pain type
    145,    # resting blood pressure
    233,    # cholesterol
    1,      # fasting blood sugar
    2,      # resting ECG
    150,    # maximum heart rate
    0,      # exercise induced angina
    2.3,    # oldpeak
    3,      # slope
    0,      # number of major vessels
    6       # thalassemia
]])


# Handle missing values
patient = imputer.transform(patient)

# Scale the input
patient = scaler.transform(patient)


# Make prediction
probability = model.predict(patient, verbose=0)[0][0]

prediction = 1 if probability >= 0.5 else 0


# Display result
print("\n-----------------------------")
print("HEART DISEASE PREDICTION")
print("-----------------------------")

print(f"Probability: {probability * 100:.2f}%")

if prediction == 1:
    print("Prediction: HEART DISEASE DETECTED")
else:
    print("Prediction: NO HEART DISEASE DETECTED")

print("-----------------------------")