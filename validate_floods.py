import csv
import os

def validate_floods_csv(filepath):
    expected_columns = [
        "MonsoonIntensity", "TopographyDrainage", "RiverManagement", "Deforestation", "Urbanization",
        "ClimateChange", "DamsQuality", "Siltation", "AgriculturalPractices", "Encroachments",
        "IneffectiveDisasterPreparedness", "DrainageSystems", "CoastalVulnerability", "Landslides",
        "Watersheds", "DeterioratingInfrastructure", "PopulationScore", "WetlandLoss",
        "InadequatePlanning", "PoliticalFactors", "FloodProbability"
    ]

    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # Check if the file has a valid header
        if reader.fieldnames is None:
            print("❌ CSV file appears to be empty or missing a header row.")
            return

        # Check for missing columns
        missing_cols = [col for col in expected_columns if col not in reader.fieldnames]
        if missing_cols:
            print(f"❌ Missing columns: {missing_cols}")
            return

        # Validate row values
        for row_num, row in enumerate(reader, start=2):  # start=2 to account for header
            for col in expected_columns[:-1]:  # all except FloodProbability
                try:
                    val = int(row[col])
                    if not (0 <= val <= 10):
                        print(f"⚠️ Row {row_num}: '{col}' has out-of-range value: {val}")
                except ValueError:
                    print(f"⚠️ Row {row_num}: '{col}' is not an integer.")

            try:
                prob = float(row["FloodProbability"])
                if not (0.0 <= prob <= 1.0):
                    print(f"⚠️ Row {row_num}: FloodProbability out of range: {prob}")
            except ValueError:
                print(f"⚠️ Row {row_num}: FloodProbability is not a float.")

        print("✅ Flood CSV validation complete.")

