from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "heart_disease_ann.keras"
)

model = load_model(MODEL_PATH)

FEATURES = [
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
    "thal"
]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Heart Disease Prediction API is running!"
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No input data received"
            }), 400

        values = []

        for feature in FEATURES:

            if feature not in data:
                return jsonify({
                    "error": f"Missing feature: {feature}"
                }), 400

            values.append(float(data[feature]))

        input_data = np.array(values, dtype=np.float32).reshape(1, -1)

        prediction = model.predict(input_data, verbose=0)

        probability = float(prediction[0][0])

        if probability >= 0.5:
            result = "Heart Disease Detected"
            status = "danger"
        else:
            result = "No Heart Disease Detected"
            status = "safe"

        return jsonify({
            "prediction": result,
            "probability": round(probability * 100, 2),
            "status": status
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
    