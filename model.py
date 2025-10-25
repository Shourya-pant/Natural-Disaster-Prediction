import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle


earthquake_path = "C:/Users/joshi/OneDrive/ドキュメント/Desktop/disasterscope/frontend/data/earthquakes.csv"
wildfire_path = "C:/Users/joshi/OneDrive/ドキュメント/Desktop/disasterscope/frontend/data/wildfires.csv"
flood_path = "C:/Users/joshi/OneDrive/ドキュメント/Desktop/disasterscope/frontend/data/floods.csv"

model_dir = "C:/Users/joshi/OneDrive/ドキュメント/Desktop/disasterscope/models"
os.makedirs(model_dir, exist_ok=True)


earthquakes = pd.read_csv(earthquake_path)
wildfires = pd.read_csv(wildfire_path)
floods = pd.read_csv(flood_path)


earthquakes = earthquakes.rename(columns={"latitude": "lat", "longitude": "lon"})
wildfires = wildfires.rename(columns={"latitude": "lat", "longitude": "lon"})
floods = floods.rename(columns={"Latitude": "lat", "Longitude": "lon"})


earthquakes["label"] = 1
wildfires["label"] = 1
floods["label"] = 1


def generate_negative_samples(df, count):
    np.random.seed(42)
    lat_range = (df["lat"].min() - 5, df["lat"].max() + 5)
    lon_range = (df["lon"].min() - 5, df["lon"].max() + 5)
    data = {
        "lat": np.random.uniform(lat_range[0], lat_range[1], count),
        "lon": np.random.uniform(lon_range[0], lon_range[1], count),
        "label": 0
    }
    return pd.DataFrame(data)


def train_and_save_model(data, filename):
    X = data[["lat", "lon"]]
    y = data["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print(f"\n📊 Report for {filename}")
    print(classification_report(y_test, preds))

    # Save model
    with open(os.path.join(model_dir, filename), "wb") as f:
        pickle.dump(clf, f)
    print(f"✅ Model saved to {filename}")


eq_neg = generate_negative_samples(earthquakes, len(earthquakes))
eq_data = pd.concat([earthquakes[["lat", "lon", "label"]], eq_neg], ignore_index=True)
train_and_save_model(eq_data, "earthquake_model.pkl")


wf_neg = generate_negative_samples(wildfires, len(wildfires))
wf_data = pd.concat([wildfires[["lat", "lon", "label"]], wf_neg], ignore_index=True)
train_and_save_model(wf_data, "wildfire_model.pkl")


flood_neg = generate_negative_samples(floods, len(floods))
flood_data = pd.concat([floods[["lat", "lon", "label"]], flood_neg], ignore_index=True)
train_and_save_model(flood_data, "flood_model.pkl")

print("\n🎉 All models trained and saved successfully.")
