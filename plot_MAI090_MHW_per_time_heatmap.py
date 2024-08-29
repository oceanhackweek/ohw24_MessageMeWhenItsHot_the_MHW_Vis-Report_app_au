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
MHW_CAT = MAI090['MHW_EVENT_CAT'].copy()

# get TEMP during the MHWs
MHW_TEMP = MAI090['TEMP_INTERP'].where(MAI090['TEMP_EXTREME_INDEX'] == 12)

# combined
combined = xr.Dataset()
combined['MHW-CAT'] = MHW_CAT
combined['MHW-TEMP'] = MHW_TEMP

# %% -------------------------------------------------------------------
# Function to split the data set into year and depth
# Have a heatmap for each year and depth, saved inside a dictionary called 'split'

# def split_by_year_and_depth(temp_dataarray):
#     """
#     Splits the temperature data into year and depth.
    
#     Parameters:
#     temp_dataarray (xarray.DataArray): The temperature dataarray with time as one of the coordinates.
    
#     Returns:
#     tuple: A tuple containing the year and depth dataarrays.
    
#     """
#     # identify number of years in data set
#     years = pd.to_datetime(temp_dataarray['TIME']).year
#     nY = np.unique(years)
#     # identify number of depths
#     nD = temp_dataarray.shape[1]
#     depths = temp_dataarray['DEPTH'].values
    
#     # megaloop to split data into day x month format for each year and depth
#     split = {}
#     for yr in nY:
#         print(yr)
#         for dep in range(nD):
#             yr_selection = years == yr
#             split[str(yr) + '_' + str(int(depths[dep])) + 'm'] = \
#                 organize_temperature_into_dataframe(
#                                 temp_dataarray[yr_selection,dep])
                
#     return split

# split = split_by_year_and_depth(MHW_CAT)

def split_by_year_depth_and_variable(dataset):
    """
    Splits the dataset into year, depth, and variable type.
    
    Parameters:
    dataset (xarray.Dataset): The dataset with time, depth, and multiple variables.
    
    Returns:
    dict: A dictionary with keys formatted as 'year_depthm_variable' and values as dataarrays.
    """
    # Extract unique years from the TIME coordinate
    years = pd.to_datetime(dataset['TIME'].values).year.unique()
    
    # Extract depths from the DEPTH coordinate
    depths = dataset['DEPTH'].values
    
    # Dictionary to hold the split data
    split = {}
    
    # Loop over each data variable, year, and depth
    for var_name, data_array in dataset.data_vars.items():
        for year in years:
            print(year)
            for depth in depths:
                # Select data by year and depth for the current variable
                selection = data_array.sel(TIME=data_array['TIME'].dt.year == year, DEPTH=depth)
                
                # Format key as 'year_depthm_variable'
                key = f"{year}_{int(depth)}m_{var_name}"
                
                # Store the selected data in the dictionary
                split[key] = organize_temperature_into_dataframe(selection)
    
    return split

split = split_by_year_depth_and_variable(combined)

# %% -------------------------------------------------------------------
# Create a plotly json file for the web app

# Convert the cmocean colormap to a Plotly-compatible colorscale
cmocean_colors = cmocean.cm.matter(np.linspace(0, 1, 256))
plotly_colorscale = [[i / (len(cmocean_colors) - 1), f'rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})'] for i, (r, g, b, a) in enumerate(cmocean_colors)]

# Initialize variables to store the selected year and depth
# (This will be the default heatmap when first opened)
selected_year = '2012'  # default year
selected_depth = '2m'  # default depth
selected_variable = 'MHW-CAT'  # default variable

# Create the figure
fig = go.Figure()

# Add traces for all year and depth combinations
# traces = plot/graphical objects that makes up a figure
# Loop over each item in the dictionary called 'split'
# Assuming 'split' dictionary has keys formatted as "year_depthm_variable"
for key, data in split.items():
    # Extract year, depth, and variable from the key
    parts = key.split('_')
    year = parts[0]
    depth = parts[1]  # Ensure depth includes 'm'
    variable = parts[2]

    # Determine initial visibility based on the selected year, depth, and variable
    visible = (year == selected_year and depth == selected_depth and variable == selected_variable)


    # Replace zeros with NaNs
    data = data.replace(0, np.nan)

    # Create a text array where NaNs are replaced with empty strings
    text_data = np.where(np.isnan(data), '', data.astype(str))

    # Create a heatmap object using Plotly's go.Heatmap
    heatmap = go.Heatmap(
        z=data.values,  # Assuming 'data' is a DataFrame or compatible format
        x=data.columns,  # Assuming columns represent X-axis data
        y=data.index,  # Assuming index represents Y-axis data
        colorscale=plotly_colorscale,
        zmin=np.nanmin(data.values),  # Use nanmin to ignore NaNs
        zmax=np.nanmax(data.values),  # Use nanmax to ignore NaNs
        text=text_data,
        texttemplate='%{text:.0f}',
        textfont=dict(size=18),
        showscale=False,
        visible=visible  # Set visibility based on conditions
    )

    # Add the created heatmap to the existing figure
    fig.add_trace(heatmap)

# Function to update the visibility of heatmaps based on selected year and depth
def create_visibility(selected_year, selected_depth, selected_variable):
    # Returns a list of boolean values for each key in the 'split' dictionary
    # True if the key matches the selected year and depth, False otherwise
     return [k == f"{selected_year}_{selected_depth}_{selected_variable}" for k in split.keys()]

year_buttons = [{
    "label": year,
    "method": "update",
    "args": [{
        "visible": create_visibility(year, selected_depth, selected_variable)  # Make sure selected_variable is passed
    }, {
        "title": f"Heatmaps for Year: {year}, Depth: {selected_depth}, Variable: {selected_variable}"
    }]
} for year in sorted(set(k.split('_')[0] for k in split.keys()))]

depth_buttons = [{
    "label": depth,
    "method": "update",
    "args": [{
        "visible": create_visibility(selected_year, depth, selected_variable)  # Make sure selected_variable is passed
    }, {
        "title": f"Heatmaps for Year: {selected_year}, Depth: {depth}, Variable: {selected_variable}"
    }]
} for depth in sorted(set(k.split('_')[1] for k in split.keys()))]

variable_buttons = [{
    "label": variable,
    "method": "update",
    "args": [{
        "visible": create_visibility(selected_year, selected_depth, variable)  # This is already correctly set
    }, {
        "title": f"Heatmaps for Year: {selected_year}, Depth: {selected_depth}, Variable: {variable}"
    }]
} for variable in sorted(set(k.split('_')[2] for k in split.keys()))]

# Update layout with dual dropdowns
fig.update_layout(
    plot_bgcolor='white',  # Sets the plot background to white for better readability
    paper_bgcolor='white',  # Sets the overall figure background to white
    updatemenus=[
        {
            "buttons": year_buttons,
            "direction": "down",
            "pad": {"r": 10, "t": 10},
            "showactive": True,
            "x": 0.1,
            "xanchor": "left",
            "y": 1.2,
            "yanchor": "top",
            # "title": "Select Year:"
        },
        {
            "buttons": depth_buttons,
            "direction": "down",
            "pad": {"r": 10, "t": 10},
            "showactive": True,
            "x": 0.3,
            "xanchor": "left",
            "y": 1.2,
            "yanchor": "top",
            # "title": "Select Depth:"
        },
        {
            "buttons": variable_buttons,
            "direction": "down",
            "pad": {"r": 10, "t": 10},
            "showactive": True,
            "x": 0.5,
            "xanchor": "left",
            "y": 1.2,
            "yanchor": "top",
            # "title": "Select Variable:"
        }
    ],
    # title=f"Temperature Anomalies for Year: {selected_year} and Depth: {selected_depth}",
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
fig.write_html("MAI090_MHW_per_time_heatmap.html")
fig.write_json("MAI090_MHW_per_time_heatmap.json")


# %% -------------------------------------------------------------------

# %% -------------------------------------------------------------------

# %% -------------------------------------------------------------------

