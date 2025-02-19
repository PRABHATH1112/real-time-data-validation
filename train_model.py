import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# Load collected sensor data
data = pd.read_csv("sensor_data.log", header=None, names=["timestamp", "sensor_id", "value"])

# Convert 'value' to numeric (handle missing values)
data["value"] = pd.to_numeric(data["value"], errors="coerce")
data.dropna(inplace=True)  # Remove missing values

# Train an Isolation Forest model for anomaly detection
model = IsolationForest(contamination=0.05, random_state=42)  # Assume 5% of data is anomalies
model.fit(data[["value"]])  # Train model on sensor values

# Save the trained model
joblib.dump(model, "anomaly_model.pkl")

print("✅ AI Model Trained and Saved Successfully!")
