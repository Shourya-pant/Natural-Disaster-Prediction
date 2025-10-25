import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

print("Starting flood model training...")

csv_path = "frontend/data/floods.csv"
model_dir = "backend/models"
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "flood_model.pkl")

df = pd.read_csv(csv_path)

required_columns = ['latitude', 'longitude', 'rainfall']
missing = [col for col in required_columns if col not in df.columns]
if missing:
    raise ValueError(f"Missing columns in flood data: {missing}")

df['rainfall'] = pd.to_numeric(df['rainfall'], errors='coerce')
df = df.dropna(subset=['rainfall'])

df['risk_label'] = df['rainfall'].apply(lambda x: 1 if x >= 150 else 0)

X = df[['latitude', 'longitude', 'rainfall']]
y = df['risk_label']

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("Flood model trained and saved successfully.")
