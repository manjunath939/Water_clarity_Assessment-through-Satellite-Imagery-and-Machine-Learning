# Water Clarity Assessment Using Satellite Imagery and Machine Learning

## Project Overview

This project is a web-based system that estimates water clarity using satellite imagery and machine learning.
Users can select any location on a map or enter coordinates manually. The system retrieves satellite data from Google Earth Engine, extracts spectral features, and predicts water clarity using a trained Random Forest model.

The result page displays water clarity classification, model confidence, spectral indicators, and interpretation to help understand water conditions.

---

## Features

* Interactive map to select any geographic location
* Manual coordinate input option
* Satellite data retrieval using Google Earth Engine
* Automatic feature extraction from satellite bands
* Machine learning based water clarity prediction
* NDWI based water body detection
* Interpretation of water quality indicators
* Display of location name using reverse geocoding
* User friendly result dashboard

---

## Technology Used

### Languages & Frameworks

Python
Flask (Web framework)

### Libraries

Scikit-learn
Pandas
NumPy
Requests
Earth Engine API
Joblib
OpenCV

### Development Environment

Google Earth Engine API

### Machine Learning Algorithm

Random Forest Classifier

---

## System Workflow

User selects location on map
↓
Coordinates sent to Flask backend
↓
Google Earth Engine fetches Sentinel-2 satellite data
↓
Spectral features extracted
↓
NDWI calculated to detect water
↓
Random Forest model predicts water clarity
↓
Results displayed on dashboard

---

## Water Clarity Classes

Fresh – High clarity water with low sediment
Moderate – Moderate clarity with some turbidity
Turbid – Low clarity water with high sediment content

---

## Project Structure

water_clarity_project

backend
app.py
model
predict_clarity.py

satellite
fetch_satellite.py

frontend
templates
map.html
result.html

requirements.txt
README.md
aquasat.csv

---

Dataset is too large to upload to GitHub.

Download AquaSat dataset from:
https://figshare.com/articles/dataset/AquaSat/8139383?file=18733733
## rename the downloaded filename to aquasat

Place aquasat.csv in the project root directory before running training.

## Installation

Clone the repository

git clone https://github.com/yourusername/water-clarity-project.git

Move into the project folder

cd water-clarity-project

Create virtual environment

python -m venv venv

Activate environment

Mac/Linux
source venv/bin/activate

Windows
venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

---

## Google Earth Engine Setup

Install Earth Engine API

pip install earthengine-api

Authenticate

earthengine authenticate

Initialize project in code

ee.Initialize(project="your-project-id")

---

## train model
python training/train_model.py(takes some time have some patience)

## Run the Application

Navigate to backend folder

cd backend

Start the server

python app.py

Open browser and visit

http://127.0.0.1:5000

---

## Example Use Case

Select a lake on the map or enter coordinates.
The system fetches satellite imagery, analyzes spectral features, and predicts water clarity in real time.

---

## Applications

Environmental monitoring
Agriculture irrigation planning
Fisheries management
Water resource management
Research and educational purposes

---

## Limitations

Model is trained mainly on inland water bodies such as lakes and reservoirs
Ocean water may not produce accurate results
Cloud cover may affect satellite data availability

---

## Future Improvements

Improve model accuracy with larger datasets
Add turbidity and chlorophyll estimation
Support time-series water monitoring
Integrate more satellite sources

---

## Author

Manjunath
Mini Project – Water Clarity Assessment Using Satellite Imagery and Machine Learning
