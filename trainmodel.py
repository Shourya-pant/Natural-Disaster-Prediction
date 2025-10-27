import os
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split

print("Starting earthquake model training...")

data_path = "earthquakes.csv"
model_path = "earthquake_model.pkl"

df = pd.read_csv(data_path)

required_cols = ['latitude', 'longitude', 'magnitude', 'depth']
missing = [col for col in required_cols if col not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")

df['magnitude'] = pd.to_numeric(df['magnitude'], errors='coerce')
df['depth'] = pd.to_numeric(df['depth'], errors='coerce')
df = df.dropna(subset=['latitude', 'longitude', 'magnitude', 'depth'])

df['risk_label'] = df['magnitude'].apply(lambda x: 1 if x >= 6.0 else 0)

print("Earthquake risk label distribution:")
print(df['risk_label'].value_counts())

X = df[['latitude', 'longitude', 'magnitude', 'depth']]
y = df['risk_label']

if y.nunique() < 2:
    model = DummyClassifier(strategy="constant", constant=y.iloc[0])
    model.fit(X, y)
else:
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print(f"Training accuracy: {model.score(X_train, y_train):.3f}")
    print(f"Test accuracy: {model.score(X_test, y_test):.3f}")

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"✅ Earthquake model saved to {model_path}")
