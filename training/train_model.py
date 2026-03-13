import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import numpy as np

# Load dataset
df = pd.read_csv("aquasat.csv")

# Keep required columns
df = df[["blue", "green", "red", "nir", "secchi"]]
df = df.dropna()

# Compute NDWI
df["ndwi"] = (df["green"] - df["nir"]) / (df["green"] + df["nir"])

# Convert secchi to clarity classes
def classify_secchi(secchi):
    if secchi > 4:
        return "Fresh"
    elif secchi >= 2:
        return "Moderate"
    else:
        return "Turbid"

df["clarity"] = df["secchi"].apply(classify_secchi)

# Features
X = df[["blue", "green", "red", "ndwi"]]
y = df["clarity"]

# Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "trained_model.pkl")

print("Model retrained with NDWI and saved.")