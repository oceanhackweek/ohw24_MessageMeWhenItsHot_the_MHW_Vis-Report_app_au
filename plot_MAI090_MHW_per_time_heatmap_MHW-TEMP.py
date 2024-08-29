##############################

# plot_MAI090_MHW_per_time_heatmap.py

# Author: Natalia Ribeiro
# Description: Plot MAI Percentiles (Using temp anomalies for now) Heatmap for every date, depth, and year

# %% --------------------------------------------------------------------
# Import packages

import xarray as xr
import numpy as np
import s3fs
import pandas as pd
import plotly.graph_objects as go
import cmocean

# %% --------------------------------------------------------------------
# Load data using AWS S3

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
    
    # Create an empty matrix with 31 rows and 12 columns
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
    # create dataframe with days on x-axis and months on y-axis
    df = pd.DataFrame(empty_matrix.transpose(), index=months, columns=days)
    df.index.name = 'Day'  # Set the index name to 'Day'
    
    return df

# %% --------------------------------------------------------------------
# Extract variables for heatmap

# Get MHW categories
ds = MAI090['TEMP_INTERP'].where(MAI090['TEMP_EXTREME_INDEX'] == 12)

# %% -------------------------------------------------------------------
# Function to split the data set into year and depth
# Have a heatmap for each year and depth, saved inside a dictionary called 'split'

def split_by_year_and_depth(temp_dataarray):
    """
    Splits the temperature data into year and depth.
    
    Parameters:
    temp_dataarray (xarray.DataArray): The temperature dataarray with time as one of the coordinates.
    
    Returns:
    tuple: A tuple containing the year and depth dataarrays.
    
    """
    # identify number of years in data set
    years = pd.to_datetime(temp_dataarray['TIME']).year
    nY = np.unique(years)
    # identify number of depths
    nD = temp_dataarray.shape[1]
    depths = temp_dataarray['DEPTH'].values
    
    # megaloop to split data into day x month format for each year and depth
    split = {}
    for yr in nY:
        print(yr)
        for dep in range(nD):
            yr_selection = years == yr
            split[str(yr) + '_' + str(int(depths[dep])) + 'm'] = \
                organize_temperature_into_dataframe(
                                temp_dataarray[yr_selection,dep])
                
    return split

split = split_by_year_and_depth(ds)

# %% -------------------------------------------------------------------
# Create a plotly json file for the web app

# Convert the cmocean colormap to a Plotly-compatible colorscale
cmocean_colors = cmocean.cm.matter(np.linspace(0, 1, 256))
plotly_colorscale = [[i / (len(cmocean_colors) - 1), f'rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})'] for i, (r, g, b, a) in enumerate(cmocean_colors)]

# Initialize variables to store the selected year and depth
# (This will be the default heatmap when first opened)
selected_year = '2012'  # default year
selected_depth = '2m'  # default depth

# Create the figure
fig = go.Figure()

# Add traces for all year and depth combinations
# traces = plot/graphical objects that makes up a figure
# Loop over each item in the dictionary called 'split'
for key, data in split.items():
    # Determine if this particular heatmap should be initially visible
    # It's visible only if the current key matches a predetermined year and depth
    visible = key == f"{selected_year}_{selected_depth}"

    # replace zeros with nans
    data = data.replace(0, np.nan)

    # Split the key into year and depth components
    # The key is expected to be in the format 'year_depthm', e.g., '2012_2m'
    year, depth = key.split('_')
    
    # Create a text array where NaNs are replaced with empty strings
    text_data = np.where(np.isnan(data), '', data.astype(str))

    # Create a heatmap object using Plotly's go.Heatmap
    heatmap = go.Heatmap(
                z=data,
                colorscale=plotly_colorscale,  # Use the converted colormap
                zmin=np.min(data),
                zmax=np.max(data),
                text=text_data,  # Display text only where there is data
                texttemplate='%{text:.0f}',
                textfont=dict(size=18),
                showscale=False
            )

    # Add the created heatmap to the existing figure
    fig.add_trace(heatmap)

# Function to update the visibility of heatmaps based on selected year and depth
def create_visibility(selected_year, selected_depth):
    # Returns a list of boolean values for each key in the 'split' dictionary
    # True if the key matches the selected year and depth, False otherwise
    return [k == f"{selected_year}_{selected_depth}" for k in split.keys()]

# Dropdown for Years
year_buttons = [{
    "label": year,  # Text to display on the dropdown button for each year
    "method": "update",  # The action to perform when a button is clicked
    "args": [
        {"visible": create_visibility(year, selected_depth)},  # Update the visibility of heatmaps
        {"title": f"Heatmaps for Year: {year} and Depth: {selected_depth}"}  # Update the chart title
    ]
} for year in sorted(set(k.split('_')[0] for k in split.keys()))]  # List comprehension to generate a button for each unique year

# Dropdown for Depths
depth_buttons = [{
    "label": depth,  # Text to display on the dropdown button for each depth
    "method": "update",  # The action to perform when a button is clicked
    "args": [
        {"visible": create_visibility(selected_year, depth)},  # Update the visibility of heatmaps
        {"title": f"Heatmaps for Year: {selected_year} and Depth: {depth}"}  # Update the chart title
    ]
} for depth in sorted(set(k.split('_')[1] for k in split.keys()))]  # List comprehension to generate a button for each unique depth


# Update layout with dual dropdowns
fig.update_layout(
    plot_bgcolor='white',  # Sets the plot background to white for better readability
    paper_bgcolor='white',  # Sets the overall figure background to white
    updatemenus=[  # Configures the dropdown menus for user interactivity
        {
            "buttons": year_buttons,  # Buttons created previously for selecting years
            "direction": "down",  # Dropdown expands downwards
            "pad": {"r": 10, "t": 10},  # Padding around the dropdown
            "showactive": True,  # Highlights the active button
            "x": 0.6,  # X position of the dropdown (percentage of the total width)
            "xanchor": "left",  # Anchor the dropdown at this x position
            "y": 1.09,  # Y position of the dropdown (percentage above the plot area)
            "yanchor": "top"  # Anchor the dropdown at this y position
        },
        {
            "buttons": depth_buttons,  # Buttons created for selecting depths
            "direction": "down",
            "pad": {"r": 10, "t": 10},
            "showactive": True,
            "x": 0.7,  # Slightly to the right of the year dropdown
            "xanchor": "left",
            "y": 1.09,
            "yanchor": "top"
        }
    ],
    title=f"Temperature Anomalies for Year: {selected_year} and Depth: {selected_depth}",
    xaxis=dict(tickangle=0),  # Ensuring x-axis labels are horizontal
    yaxis=dict(autorange='reversed')  # Invert y-axis so higher values appear lower
)

# Additional updates to layout properties for axis settings
fig.update_layout(
    xaxis=dict(
        title="Day",  # Label for the x-axis
        tickmode='array',  # Explicitly specify tick positions and labels
        tickvals=list(range(1, len(data.columns) + 1)),  # Positions for x-axis ticks
        ticktext=data.columns,  # Text labels for x-axis ticks
        tickangle=0  # Keep x-axis labels horizontal
        # range=[0, 31]  # Optionally set the range of the x-axis
    ),
    yaxis=dict(
        title="Month",  # Label for the y-axis
        tickmode='array',  # Explicitly specify tick positions and labels
        tickvals=list(range(len(data.index))),  # Positions for y-axis ticks
        ticktext=data.index,  # Text labels for y-axis ticks
        # range=[0, 12]  # Optionally set the range of the y-axis
    ),
    font=dict(size=18)  # Set the global font size for text elements
)

# Show figure
fig.show()

# Save the figure as an HTML file
fig.write_html("MAI090_MHW_per_time_heatmap_TEMP-ANOM.html")
fig.write_json("MAI090_MHW_per_time_heatmap_TEMP-ANOM.json")


# %% -------------------------------------------------------------------

# %% -------------------------------------------------------------------

# %% -------------------------------------------------------------------