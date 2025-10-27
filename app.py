import flask
from flask import Flask, jsonify, request, render_template
import os
import pickle
import pandas as pd
from math import radians, cos, sin, sqrt, atan2


app = Flask(__name__)


earthquake_model = pickle.load(open("earthquake_model.pkl", "rb"))
flood_model = pickle.load(open("flood_model.pkl", "rb"))
wildfire_model = pickle.load(open("wildfire_model.pkl", "rb"))


earthquakes_df = pd.read_csv("earthquakes.csv")
floods_df = pd.read_csv("floods.csv")
wildfires_df = pd.read_csv("wildfires.csv")

wildfires_df['Fires'] = wildfires_df['Fires'].replace(',', '', regex=True).astype(int)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


def count_nearby(df, lat, lon, radius_km=100):
    count = 0
    for _, row in df.iterrows():
        dist = haversine(lat, lon, row['latitude'], row['longitude'])
        if dist <= radius_km:
            count += 1
    return count

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    if lat is None or lng is None:
        return jsonify({"error": "Missing lat or lng parameters"}), 400

    eq_magnitude = earthquakes_df['magnitude'].mean()
    eq_depth = earthquakes_df['depth'].mean()
    eq_input = [[lat, lng, eq_magnitude, eq_depth]]

    flood_rainfall = floods_df['rainfall'].mean()
    flood_input = [[lat, lng, flood_rainfall]]

    avg_fires = wildfires_df['Fires'].mean()
    wildfire_input = [[avg_fires]]

    earthquake_prob = earthquake_model.predict_proba(eq_input)[0][1] * 100
    flood_prob = flood_model.predict_proba(flood_input)[0][1] * 100
    wildfire_prob = wildfire_model.predict_proba(wildfire_input)[0][1] * 100

    eq_count = count_nearby(earthquakes_df, lat, lng, 100)
    flood_count = count_nearby(floods_df, lat, lng, 100)
    wildfire_count = len(wildfires_df)

    return jsonify({
        "earthquake": round(earthquake_prob, 2),
        "flood": round(flood_prob, 2),
        "wildfire": round(wildfire_prob, 2),
        "counts": {
            "earthquake": eq_count,
            "flood": flood_count,
            "wildfire": wildfire_count
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
