import joblib
import pandas as pd

model = joblib.load("trained_model.pkl")

def rule_based_refinement(prediction, features):

    # Use NDWI instead of green-blue comparison
    if features["ndwi"] < 0.3:
        return "Turbid"

    return prediction


def predict_water_clarity(features):

    input_df = pd.DataFrame([{
        "blue": features["blue"],
        "green": features["green"],
        "red": features["red"],
        "ndwi": features["ndwi"]
    }])

    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)

    print("Prediction probabilities:", proba)

    final_prediction = rule_based_refinement(prediction, features)

    return final_prediction