import pickle
import os


model_path = os.path.join(os.path.dirname(__file__), "../models/disaster_predictor.pkl")


with open(model_path, "rb") as f:
    ml_model = pickle.load(f)

def ml_predict_earthquake_risk(lat, lng):
    import pandas as pd
    prob = ml_model.predict_proba(pd.DataFrame([[lat, lng]], columns=["latitude", "longitude"]))[0][1]
    return round(prob * 100, 2)
