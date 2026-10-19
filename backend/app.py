
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Locate the saved model in the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_DIR / "airline_rf_model.joblib"

saved_data = joblib.load(MODEL_PATH)

model = saved_data["model"]
feature_columns = saved_data["feature_columns"]
arrival_delay_median = saved_data["arrival_delay_median"]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Airline Satisfaction API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Please send a JSON object"}), 400

    try:
        # Convert the received passenger details into a DataFrame
        df = pd.DataFrame([data])

        # Fill a missing arrival delay with the training median
        if "Arrival Delay in Minutes" not in df.columns:
            df["Arrival Delay in Minutes"] = arrival_delay_median

        df["Arrival Delay in Minutes"] = pd.to_numeric(
            df["Arrival Delay in Minutes"], errors="raise"
        ).fillna(arrival_delay_median)

        # Encode the categorical fields just as during training
        categorical_columns = [
            "Gender",
            "Customer Type",
            "Type of Travel",
            "Class"
        ]

        df = pd.get_dummies(
            df,
            columns=[
                col for col in categorical_columns if col in df.columns
            ],
            drop_first=True
        )

        # Ensure the input has every expected feature in the correct order
        df = df.reindex(columns=feature_columns, fill_value=0)

        # Make the prediction
        prediction = int(model.predict(df)[0])
        probability = model.predict_proba(df)[0].tolist()

        label = (
            "Satisfied" if prediction == 1
            else "Neutral or dissatisfied"
        )

        return jsonify({
            "prediction": prediction,
            "satisfaction": label,
            "probabilities": {
                "neutral_or_dissatisfied": probability[0],
                "satisfied": probability[1]
            }
        })

    except (ValueError, TypeError) as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
