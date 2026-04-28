import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("🔹 Loading cleaned dataset...")
df = pd.read_csv("dataset/clean_data.csv")

# 🔥 Sample data for faster training (recommended)
print("🔹 Sampling dataset...")
df = df.sample(n=200000, random_state=42)

print(f"🔹 Dataset size after sampling: {df.shape}")

# Separate features and label
print("🔹 Preparing features and labels...")
X = df.drop("Label", axis=1)
y = df["Label"]

# Train-test split
print("🔹 Splitting dataset into train and test...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create Random Forest model
print("🔹 Initializing Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1  # Use all CPU cores
)

# Train model
print("🚀 Training model (this may take a minute)...")
model.fit(X_train, y_train)

print("✅ Training completed!")

# Predict on test set
print("🔹 Making predictions...")
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Model Accuracy: {accuracy * 100:.2f}%\n")

# Classification report
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))

# Save trained model
joblib.dump(model, "network_model.pkl")
print("💾 Model saved as network_model.pkl")