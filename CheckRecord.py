# %% ---------------------------------------------
# Load packages

import json
import pickle as pkl
import numpy as np
from datetime import datetime
import runpy
import glob
import os

# %% ---------------------------------------------
# Check available pickle files and identify the most recent one and, if available, the previous one

save_directory = r"New_data"  # Updated path

# List all pickle files in the directory
pickle_files = glob.glob(os.path.join(save_directory, "*.pkl"))

# Get file creation dates and times in numpy datetime64 format
file_dates = [
    np.datetime64(
        datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%dT%H:%M")
    )
    for file in pickle_files
]

# Check if there are at least two files to compare
if len(pickle_files) < 2:
    print("Not enough files to compare.")
    send_email = False
else:
    # Extract the max from each file and save it in a list
    max_temp = []

    for file in pickle_files:
        with open(file, "rb") as f:
            data = pkl.load(f)
            max_temp.append(data["all_time_depth_max"])

    # Determine if the max in the most recent pickle is higher than the max in the previous one
    most_recent_file_ind = np.int32(
        np.where(file_dates == np.nanmax(file_dates))
    ).squeeze()
    previous_file_dates = np.delete(
        file_dates, most_recent_file_ind
    )  # Exclude the most recent file
    previous_file_ind = np.int32(
        np.where(file_dates == np.nanmax(previous_file_dates))
    ).squeeze()

    print("most_recent_file_ind", most_recent_file_ind)
    print("previous_file_ind", previous_file_ind)

    if max_temp[most_recent_file_ind] > max_temp[previous_file_ind]:
        send_email = True
    else:
        send_email = False

# %% ---------------------------------------------
# If the max in the most recent pickle is higher than the max in the previous one, send an email

if send_email:
    # Send an email
    runpy.run_path(r"AWS-SES-SendEmail.py")
