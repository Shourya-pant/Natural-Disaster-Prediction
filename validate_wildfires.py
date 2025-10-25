import csv

columns = ["Year", "Fires", "Acres", "ForestService", "DOIAgencies", "Total"]

def clean_number(value):
    return value.replace(",", "").replace("$", "").strip()

def is_valid_int(value):
    try:
        int(value)
        return True
    except:
        return False

def is_valid_float(value):
    try:
        float(value)
        return True
    except:
        return False

def validate_row(row, line_num):
    errors = []

    # Validate Year
    if not is_valid_int(row["Year"]):
        errors.append(f"Invalid Year: {row['Year']}")

    # Validate Fires
    fires = clean_number(row["Fires"])
    if not is_valid_int(fires):
        errors.append(f"Invalid Fires count: {row['Fires']}")

    # Validate Acres
    acres = clean_number(row["Acres"])
    if not is_valid_int(acres):
        errors.append(f"Invalid Acres count: {row['Acres']}")

    # Validate ForestService
    fs = clean_number(row["ForestService"])
    if not is_valid_float(fs):
        errors.append(f"Invalid ForestService amount: {row['ForestService']}")

    # Validate DOIAgencies
    doi = clean_number(row["DOIAgencies"])
    if not is_valid_float(doi):
        errors.append(f"Invalid DOIAgencies amount: {row['DOIAgencies']}")

    # Validate Total
    total = clean_number(row["Total"])
    if not is_valid_float(total):
        errors.append(f"Invalid Total amount: {row['Total']}")

    return errors

def validate_wildfire_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        missing_cols = [col for col in columns if col not in reader.fieldnames]
        if missing_cols:
            print(f"Missing columns: {missing_cols}")
            return

        all_errors = []
        for line_num, row in enumerate(reader, start=2):
            errors = validate_row(row, line_num)
            if errors:
                all_errors.append(f"Line {line_num}: {', '.join(errors)}")

        if all_errors:
            print("Wildfire Dataset Validation Errors:")
            for err in all_errors:
                print(err)
        else:
            print("No errors found in Wildfire dataset!")

if __name__ == "__main__":
    validate_wildfire_csv("wildfires.csv")
