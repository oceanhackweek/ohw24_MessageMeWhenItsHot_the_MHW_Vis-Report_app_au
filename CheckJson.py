# %% ---------------------------------------------
# Load packages

import json
import pickle as pkl
import numpy as np
from datetime import datetime
import os

# %% ---------------------------------------------
# Instructions for Ranisa

# This script extracts the maximum temperature anomaly from the JSON file and saves the output as a pickle file

# (1) setup a trigger that runs this script when a new json file is added to the folder
# (2) change the load directory to where you have stored the json files
# (3) load the MAI090_PercentilesHeatMap.json file, run the loop
# (4) change the save directory to where you want to save the pickle file and run code to save

# Notes

# the runpy package could be used to run this script from the web app script?
# see example below:

# import runpy
# # Assuming 'my_script' is a module in your Python path
# runpy.run_path('path/to/my_script.py')

# %% ---------------------------------------------
# Load latest json plot
# Temp anomaly (called percentiles) plot

# Update the load directory path to your local path
load_directory = r"New_data"

# Full path to the JSON file
json_file_path = os.path.join(load_directory, "MAI090_PercentilesHeatMap.json")

# Load the JSON file
try:
    with open(json_file_path, "r") as file:
        heatmaps = json.load(file)
except FileNotFoundError:
    print(f"File not found: {json_file_path}")
    raise

# %% ---------------------------------------------
# Extract the data from the JSON object

data = heatmaps["data"]

# Prepare to track the maximum temperature anomalies by year
max_temps_by_year = {}

for n in range(len(data)):
    x = data[n]["x"]
    y = data[n]["y"]
    z = data[n]["z"]
    # Convert None to np.nan
    z = np.array(z, dtype=float).flatten()
    z = np.where(z == None, np.nan, z)
    name = data[n]["name"]
    year = name.split(" ")[0]
    depth = name.split(" ")[-1]

    # Find the maximum temperature anomaly in the data for this year
    if np.isfinite(z).sum() > 10:
        max_temp = np.nanmax(z)
    else:
        max_temp = np.nan
    max_temps_by_year[year] = max_temp

all_time_depth_max = np.nanmax(list(max_temps_by_year.values()))

# Output the results (optional)
# for year, max_temp in max_temps_by_year.items():
#     print(f"Year {year}: Max Temperature Anomaly {max_temp}")

# %% ---------------------------------------------
# Save variables using pickle

# Update the save directory path to the same folder as the JSON file
save_directory = load_directory  # Use the same directory as the load directory

# Get the current date and time
now = datetime.now()

# Format the date and time as 'YYYYMMDD_HHMM'
formatted_time = now.strftime("%Y%m%d_%H%M")

data_to_save = {
    "max_temps_by_year": max_temps_by_year,
    "all_time_depth_max": all_time_depth_max,
}

# Save data to a pickle file
pickle_file_path = os.path.join(save_directory, f"maxTemp{formatted_time}.pkl")
with open(pickle_file_path, "wb") as file:
    pkl.dump(data_to_save, file)
