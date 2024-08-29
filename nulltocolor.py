import json
import os

def replace_null_colors(data):
    # If the data is a list, iterate over it
    if isinstance(data, list):
        for item in data:
            replace_null_colors(item)
    # If the data is a dictionary, check for 'color' key and null values
    elif isinstance(data, dict):
        for key, value in data.items():
            if key == 'color' and isinstance(value, list):
                data[key] = ['#000000' if v is None else v for v in value]
            else:
                replace_null_colors(value)

def replace_null_values_in_json(file_path):
    # Load JSON data from the file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Replace null values under the 'color' key
    replace_null_colors(data)
    
    # Save the modified JSON back to the file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Example usage
file_path = os.path.join('Figures', 'DailyAVG_plot.json')
replace_null_values_in_json(file_path)
