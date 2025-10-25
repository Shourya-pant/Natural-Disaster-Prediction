import os
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split

print("Starting wildfire model training...")

data_path = "frontend/data/wildfires.csv"
model_dir = "backend/models"
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "wildfire_model.pkl")

df = pd.read_csv(data_path)


if 'Fires' not in df.columns:
    raise ValueError("Required column 'Fires' missing in wildfire data")


df['Fires'] = df['Fires'].astype(str).str.replace(',', '', regex=True)
df['Fires'] = pd.to_numeric(df['Fires'], errors='coerce')


df = df.dropna(subset=['Fires'])


df['risk_label'] = df['Fires'].apply(lambda x: 1 if x >= 70000 else 0)

print("Risk label distribution:")
print(df['risk_label'].value_counts())

X = df[['Fires']]
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

print(f"Wildfire model saved at: {model_path}")
