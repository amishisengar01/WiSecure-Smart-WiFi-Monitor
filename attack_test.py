import pandas as pd
import joblib

# Load model
model = joblib.load("network_model.pkl")

# Load clean dataset
df = pd.read_csv("dataset/clean_data.csv")

# 🔴 Take REAL attack sample
attack_row = df[df["Label"] == 1].sample(1, random_state=1)

# Remove label
X_attack = attack_row.drop("Label", axis=1)

# 🔥 Ensure SAME feature order as training
X_attack = X_attack[model.feature_names_in_]

print("Using real attack sample:")
print(X_attack)

pred = model.predict(X_attack)[0]

if pred == 1:
    print("🔴 ATTACK DETECTED (High Risk)")
else:
    print("🟢 SAFE (Low Risk)")