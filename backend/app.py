print("APP STARTED")

from flask import Flask, request, render_template
print("Flask imported")

from satellite.fetch_satellite import fetch_satellite_features
print("Satellite module imported")

from model.predict_clarity import model
print("Model imported")

import pandas as pd
import requests
from flask import redirect, url_for


def get_location_name(lat, lon):

    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"

    headers = {
        "User-Agent": "water-clarity-project"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "Unknown Location")

    except:
        pass

    return "Unknown Location"


app = Flask(
    __name__,
    template_folder="../frontend/templates"
)

print("Starting Flask server...")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/map")
def map_page():
    error_message = request.args.get("error_message")
    return render_template("map.html", error_message=error_message)


@app.route("/receive-coordinates", methods=["POST"])
def receive_coordinates():

    data = request.json

    latitude = float(data.get("latitude"))
    longitude = float(data.get("longitude"))

    location_name = get_location_name(latitude, longitude)

    # STEP 1: Try fetching satellite features
    try:

        features = fetch_satellite_features(latitude, longitude)

    except Exception as e:

        return render_template(
            "result.html",
            prediction="Satellite Data Unavailable",
            confidence=0,
            ndwi=0,
            red=0,
            location=location_name,
            latitude=latitude,
            longitude=longitude,
            ndwi_text="Satellite image could not be retrieved.",
            red_text="Possible reasons: cloud cover, no recent image, or API limitation."
        )

    # STEP 2: Check if location contains water
    if features["ndwi"] < 0.2:

        return redirect(url_for(
            "map_page",
            error_message="The selected landmark does not contain a water body. Please choose a lake, river, or reservoir."
        ))

    # STEP 3: Prepare ML input
    input_df = pd.DataFrame([{
        "blue": features["blue"],
        "green": features["green"],
        "red": features["red"],
        "ndwi": features["ndwi"]
    }])

    prediction = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]

    confidence = round(max(probabilities) * 100, 2)

    ndwi = features["ndwi"]
    red = features["red"]

    # Interpretation
    if ndwi > 0.6:
        ndwi_text = "High NDWI → Strong water presence and likely clear water."

    elif ndwi > 0.3:
        ndwi_text = "Moderate NDWI → Water detected but possible turbidity."

    else:
        ndwi_text = "Low NDWI → Weak water signal."

    if red < 100:
        red_text = "Low Red reflectance → Low suspended sediment."

    elif red < 400:
        red_text = "Moderate Red reflectance → Some sediment present."

    else:
        red_text = "High Red reflectance → High sediment or turbidity."

    return render_template(
        "result.html",
        prediction=prediction,
        confidence=confidence,
        ndwi=round(ndwi, 3),
        red=round(red, 2),
        location=location_name,
        latitude=latitude,
        longitude=longitude,
        ndwi_text=ndwi_text,
        red_text=red_text
    )


if __name__ == "__main__":
    app.run(debug=True)