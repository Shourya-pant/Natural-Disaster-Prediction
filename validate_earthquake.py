import csv
from datetime import datetime

def validate_row(row, line_num):
    errors = []

    # Helper to check float
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    # Helper to check int
    def is_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    # Validate columns
    # title (text, non-empty)
    if not row['title'] or not isinstance(row['title'], str):
        errors.append("title missing or invalid")

    # magnitude (float)
    if not is_float(row['magnitude']):
        errors.append("magnitude not a valid float")

    # date_time (dd-mm-yyyy HH:MM)
    try:
        datetime.strptime(row['date_time'].strip(), "%d-%m-%Y %H:%M")
    except ValueError:
        try:
            datetime.strptime(row['date_time'].strip(), "%d-%m-%Y %H:%M:%S")
        except ValueError:
            errors.append("date_time not in dd-mm-yyyy HH:MM or HH:MM:SS format")

    # cdi (int or empty)
    if row['cdi'].strip() and not is_int(row['cdi']):
        errors.append("cdi not an integer or empty")

    # mmi (int or empty)
    if row['mmi'].strip() and not is_int(row['mmi']):
        errors.append("mmi not an integer or empty")

    # alert (empty or green/yellow/red)
    if row['alert'].strip() and row['alert'].strip().lower() not in ['green', 'yellow', 'red']:
        errors.append("alert not one of green, yellow, red, or empty")

    # tsunami (int)
    if not is_int(row['tsunami']):
        errors.append("tsunami not an integer")

    # sig (int)
    if not is_int(row['sig']):
        errors.append("sig not an integer")

    # net (string, non-empty)
    if not row['net'].strip():
        errors.append("net missing or empty")

    # nst (int or empty)
    if row['nst'].strip() and not is_int(row['nst']):
        errors.append("nst not an integer or empty")

    # dmin (float or empty)
    if row['dmin'].strip() and not is_float(row['dmin']):
        errors.append("dmin not a float or empty")

    # gap (int or empty)
    if row['gap'].strip() and not is_int(row['gap']):
        errors.append("gap not an integer or empty")

    # magType (non-empty string)
    if not row['magType'].strip():
        errors.append("magType missing or empty")

    # depth (float)
    if not is_float(row['depth']):
        errors.append("depth not a float")

    # latitude (float)
    if not is_float(row['latitude']):
        errors.append("latitude not a float")

    # longitude (float)
    if not is_float(row['longitude']):
        errors.append("longitude not a float")

    # location (non-empty string)
    if not row['location'].strip():
        errors.append("location missing or empty")

    # continent (string or empty)
    # no strict validation here, just allow empty or string

    # country (string or empty)
    # no strict validation here, just allow empty or string

    return errors


def validate_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        all_errors = []
        for line_num, row in enumerate(reader, start=2):  # header line is 1
            errors = validate_row(row, line_num)
            if errors:
                all_errors.append(f"Line {line_num}: {', '.join(errors)}")

        if all_errors:
            print("Validation Errors found:")
            for err in all_errors:
                print(err)
        else:
            print("No errors found. CSV is valid!")


if __name__ == "__main__":
    # Put your earthquake.csv file path here
    
    validate_csv ("earthquakes.csv")
                
