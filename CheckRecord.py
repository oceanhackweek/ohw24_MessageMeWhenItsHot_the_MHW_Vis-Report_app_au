# %% ---------------------------------------------
# Load packages

import json
import pickle as pkl
import numpy as np
from datetime import datetime
import runpy
import glob
import re

# %% ---------------------------------------------
# Instructions for Ranisa

# This script checks the most recent max temp anomaly pickle file with the previous one. If the max temp
# anomaly exists in the most recent one, an email is sent to subscribers (Michael for now)

# (1) setup a trigger that runs this script after the 'CheckJson.py' file has finished
# (2) update save_directory to the path where the pickle files are stored
# (3) update directory where 'AWS-SES-SendEmail.py' script is stored
# (4) run script to test


# Notes

# the runpy package could be used to run this script from the web app script?
# see example below:

# import runpy
# # Assuming 'my_script' is a module in your Python path
# runpy.run_path('path/to/my_script.py')

# %% ---------------------------------------------
# check available pickle files and identify the most recent one and if available the previous one

save_directory = r'C:\Users\mphem\OneDrive - UNSW\Work\OHW\ohw24_OceanExtremes_VisReportApp_au\New_data'

# List all pickle files in the directory
pickle_files = glob.glob(os.path.join(save_directory, '*.pkl'))

# Get file creation dates and times in numpy datetime64 format
file_dates = [np.datetime64(datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%dT%H:%M:%S.%f')) for file in pickle_files]


# Extract datetime from filenames and convert to numpy.datetime64
file_dates = []
for file in pickle_files:
    # Extract the datetime part from the filename
    match = re.search(r'maxTemp_(\d{8}_\d{6})\.pkl', os.path.basename(file))
    if match:
        datetime_str = match.group(1)
        # Reformat to ISO 8601 standard for conversion
        datetime_iso = datetime_str[0:4] + '-' + datetime_str[4:6] + '-' + datetime_str[6:8] + ' ' + datetime_str[9:11] + ':' + datetime_str[11:13] + ':' + datetime_str[13:15]
        # Convert to numpy.datetime64
        datetime_np = np.datetime64(datetime_iso)
        file_dates.append(datetime_np)

print(file_dates)

# %% ---------------------------------------------
# Extract the max from each file and save it in a list

max_temp = []

for file in pickle_files:
    with open(file, 'rb') as f:
        data = pkl.load(f)
        
        max_temp.append(data['all_time_depth_max'])

# %% ---------------------------------------------
# Determine if the max in the most recent pickle is higher than the max in the previous one

most_recent_file_ind = np.int32(np.where(file_dates == np.nanmax(file_dates))).squeeze()
previous_file_ind = np.int32(np.where(file_dates != np.nanmax(file_dates))).squeeze()

print(max_temp[most_recent_file_ind])
print(max_temp[previous_file_ind])

if max_temp[most_recent_file_ind] > max_temp[previous_file_ind]:
    send_email = True
else:
    send_email = False

# %% ---------------------------------------------
# if the max in the most recent pickle is higher than the max in the previous one send an email

if send_email:
    # send an email
    runpy.run_path(r'C:\Users\mphem\OneDrive - UNSW\Work\OHW\ohw24_OceanExtremes_VisReportApp_au\AWS-SES-SendEmail.py')
# %%
