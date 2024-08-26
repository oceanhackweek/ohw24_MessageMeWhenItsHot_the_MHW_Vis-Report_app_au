##############################

# plot_MAI_PercentilesHeatMap.py

# Author: Michael Hemming
# Description: Plot MAI Percentiles Heatmap for every date, depth, and year

# %% --------------------------------------------------------------------
# Import packages

import xarray as xr
import seaborn as sns
import numpy as np
import s3fs
import pandas as pd
import plotly.tools as tls
import plotly.io as pio
import cmocean
import matplotlib.pyplot as plt

# %% --------------------------------------------------------------------
# Load data

s3 = s3fs.S3FileSystem(anon=True) 

bucket_prefix = "imos-data/UNSW/NRS_extremes/Temperature_DataProducts_v2/"
MAI090 = xr.open_dataset(s3.open(bucket_prefix + "MAI090/MAI090_TEMP_EXTREMES_1944-2023_v2.nc"))

# %% --------------------------------------------------------------------
# Function to organise data into a day x month matrix for a selected year

def organize_temperature_into_dataframe(temp_dataarray):
    """
    Organizes temperature data into a DataFrame where rows are days of the month and columns are months.
    
    Parameters:
    temp_dataarray (xarray.DataArray): The temperature dataarray with time as one of the coordinates.
    empty_matrix (numpy.ndarray): The matrix to be filled with temperatures.

    Returns:
    pandas.DataFrame: The filled DataFrame with temperatures.
    """
    
    empty_matrix = np.ones((31,12)) * np.nan
    
    # Iterate over the temperature data
    for i in range(temp_dataarray.shape[0]):
        # Extract the date and corresponding day/month
        date = temp_dataarray.TIME[i].values
        day = np.datetime64(date, 'D').astype(object).day
        month = np.datetime64(date, 'M').astype(object).month
        
        # Fill the matrix at the corresponding day-1 (0-index) and month-1 (0-index) position
        empty_matrix[day - 1, month - 1] = temp_dataarray[i].values
    
    # Convert the matrix to a pandas DataFrame
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    days = list(range(1, 32))  # Days of the month (1 to 31)

    df = pd.DataFrame(empty_matrix.transpose(), index=months, columns=days)
    df.index.name = 'Day'  # Set the index name to 'Day'
    
    return df


# Example usage with a DataArray and an empty matrix
ds = MAI090['TEMP'].sel(
    TIME=slice('2022-01-01', '2022-12-31')).copy()
ds.values = MAI090['TEMP'].sel(
    TIME=slice('2022-01-01', '2022-12-31')).values - MAI090['TEMP_MEAN'].sel(
                        TIME=slice('2022-01-01', '2022-12-31')).values

Tanom = organize_temperature_into_dataframe(ds[:,1])

# create heatmap
plt.figure(figsize=(24,12))
sns.heatmap(np.round(Tanom,2), annot=True, cmap=cmocean.cm.balance, 
            cbar_kws={'label': 'Temperature Anomaly'},  # Optional: Add colorbar label
            xticklabels=1, yticklabels=1, cbar=False, 
            annot_kws={"fontsize": 18}, linewidths=1, linecolor='black'  # Control the frequency of tick labels
            )

# Increase the fontsize of the tick labels, 
plt.xticks(fontsize=30)
plt.yticks(fontsize=30, rotation=360)
plt.ylabel('')

plt.tight_layout()

# import plotly.graph_objects as go

# # Create a heatmap using Plotly
# fig = go.Figure(data=go.Heatmap(
#     z=np.round(Tanom, 2),
#     colorscale=cmocean.cm.balance(np.linspace(0, 1, 256)),  # Use the same colormap
#     colorbar=dict(title='Temperature Anomaly', tickvals=np.linspace(np.min(Tanom), np.max(Tanom), 5)),  # Colorbar settings
#     zmin=np.min(Tanom),  # Set min and max to match your data range
#     zmax=np.max(Tanom),
#     text=np.round(Tanom, 2),  # Add annotations
#     texttemplate='%{text}',
#     textfont=dict(size=18),
#     showscale=True
# ))

# # Update layout for axis titles and tick labels
# fig.update_layout(
#     xaxis=dict(
#         tickfont=dict(size=30),
#         title='',
#     ),
#     yaxis=dict(
#         tickfont=dict(size=30),
#         title='',
#         tickvals=np.arange(Tanom.shape[0]),  # Set tick values if needed
#         ticktext=[str(i) for i in range(Tanom.shape[0])]  # Replace with actual y-tick labels
#     ),
#     title='Heatmap',
#     title_x=0.5,
#     title_font=dict(size=30),
# )

# # Show figure
# fig.show()



# %% --------------------------------------------------------------------
# convert figure to plotly html

# Step 2: Convert the Matplotlib figure to a Plotly figure
plotly_fig = tls.mpl_to_plotly(plt.gcf())

# Step 3: Save the Plotly figure as an HTML file
pio.write_html(plotly_fig, file='PercentilesHeatMap.html', auto_open=True)

# Show the Matplotlib plot
plt.show()
