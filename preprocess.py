import pandas as pd

# Load merged dataset
df = pd.read_csv("dataset/merged_data.csv")

# Remove leading/trailing spaces from column names
df.columns = df.columns.str.strip()

print("Columns cleaned successfully")

# Select valid & important columns
df = df[[
    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Packet Length Mean",
    "Label"
]]

# Convert labels (BENIGN = 0, Attack = 1)
df["Label"] = df["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

# Remove infinite values
df = df.replace([float('inf'), float('-inf')], None)

# Drop missing values
df = df.dropna()

# Save cleaned dataset
df.to_csv("dataset/clean_data.csv", index=False)

print("✅ Clean dataset saved as clean_data.csv")