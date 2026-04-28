import joblib
import pandas as pd

# Load model
model = joblib.load("network_model.pkl")

# Sample input (same feature order as training)
sample = pd.DataFrame([{
    "Destination Port": 4444,          # Suspicious / uncommon port
    "Flow Duration": 10,               # Very short duration (burst attack)
    "Total Fwd Packets": 5000,         # Extremely high forward packets
    "Total Backward Packets": 4000,    # High response traffic
    "Packet Length Mean": 1500         # Very large packet size
}])

prediction = model.predict(sample)[0]
def risk_score(pred):
    return "Low Risk (0–30)" if pred == 0 else "High Risk (70–100)"

if prediction == 0:
    print("🟢 Network Traffic: SAFE")
else:
    print("🔴 Network Traffic: ATTACK DETECTED")