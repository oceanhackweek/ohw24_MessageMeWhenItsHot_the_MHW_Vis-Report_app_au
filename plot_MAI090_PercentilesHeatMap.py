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
import plotly.graph_objects as go

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

Tanom1 = organize_temperature_into_dataframe(ds[:,1])
Tanom0 = organize_temperature_into_dataframe(ds[:,0])
# create heatmap
plt.figure(figsize=(24,12))
sns.heatmap(np.round(Tanom1,2), annot=True, cmap=cmocean.cm.balance, 
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

# Create the heatmap using Plotly
fig = go.Figure(data=go.Heatmap(
    z=Tanom1.values,
    x=Tanom1.columns,
    y=Tanom1.index,
    colorscale='balance',  # Use the cmocean balance colormap
    colorbar=dict(
        title='Temperature Anomaly',
        titleside='right',
        titlefont=dict(size=18),
        tickfont=dict(size=18)
    ),
    zmin=-2,  # Set the minimum value for the color scale
    zmax=2,   # Set the maximum value for the color scale
    showscale=False  # Hide colorbar if you don't need it
))

# Update layout for axis titles and tick labels
fig.update_layout(
    xaxis=dict(
        tickfont=dict(size=30),
        title='',
    ),
    yaxis=dict(
        tickfont=dict(size=30),
        title='',
        tickvals=np.arange(Tanom.shape[0]),  # Set tick values if needed
        ticktext=[str(i) for i in range(Tanom.shape[0])]  # Replace with actual y-tick labels
    ),
    title='Heatmap',
    title_x=0.5,
    title_font=dict(size=30),
)

# Show figure
fig.show()

# %% ------------------------------------------------------------------
# get TEMP anom (all time)

ds = MAI090['TEMP'].copy()
ds.values = MAI090['TEMP'].values - MAI090['TEMP_MEAN'].values





# %% -------------------------------------------------------------------
# Function to split the data set into year and depth

temp_dataarray = ds

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


split = split_by_year_and_depth(temp_dataarray)

# %% -------------------------------------------------------------------

# Initialize variables to store the selected year and depth
selected_year = '2012'  # default year
selected_depth = '2m'  # default depth

# Create the figure
fig = go.Figure()

# Add traces for all year and depth combinations
for key, data in split.items():
    visible = key == f"{selected_year}_{selected_depth}"
    year, depth = key.split('_')
    heatmap = go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale='balance',
        showscale=False,
        zmin=-2, zmax=2,
        visible=visible,  # Control initial visibility
        name=f"{year} - {depth}"
    )
    fig.add_trace(heatmap)

# Function to update the visibility of heatmaps based on selected year and depth
def create_visibility(selected_year, selected_depth):
    return [k == f"{selected_year}_{selected_depth}" for k in split.keys()]

# Dropdown for Years
year_buttons = [{
    "label": year,
    "method": "update",
    "args": [{"visible": create_visibility(year, selected_depth)},
             {"title": f"Heatmaps for Year: {year} and Depth: {selected_depth}"}]
} for year in sorted(set(k.split('_')[0] for k in split.keys()))]

# Dropdown for Depths
depth_buttons = [{
    "label": depth,
    "method": "update",
    "args": [{"visible": create_visibility(selected_year, depth)},
             {"title": f"Heatmaps for Year: {selected_year} and Depth: {depth}"}]
} for depth in sorted(set(k.split('_')[1] for k in split.keys()))]

# Update layout with dual dropdowns
fig.update_layout(
    plot_bgcolor='white',  # Sets the plot background to white
    paper_bgcolor='white',  # Sets the overall figure background to white
    updatemenus=[
        {"buttons": year_buttons, "direction": "down", "pad": {"r": 10, "t": 10},
         "showactive": True, "x": 0.6, "xanchor": "left", "y": 1.09, "yanchor": "top"},
        {"buttons": depth_buttons, "direction": "down", "pad": {"r": 10, "t": 10},
         "showactive": True, "x": 0.7, "xanchor": "left", "y": 1.09, "yanchor": "top"}
    ],
    title=f"Temperature Anomalies for Year: {selected_year} and Depth: {selected_depth}",
    xaxis=dict(tickangle=0),  # Ensuring x-axis labels are horizontal
    yaxis=dict(autorange='reversed')  # Invert y-axis
)

# Update layout properties
fig.update_layout(
    xaxis=dict(
        title="Day",
        tickmode='array',
        tickvals=list(range(1,len(Tanom0.columns)+1)),  # Ensure every x-tick has a label
        ticktext=Tanom0.columns,  # Custom text for each tick, matching the column labels
        tickangle=0,
        # range=[0, 31]
    ),
    yaxis=dict(
        title="Month",
        tickmode='array',
        tickvals=list(range(len(Tanom0.index))),  # Ensure every y-tick has a label
        ticktext=Tanom0.index,  # Custom text for each tick, matching the index labels
        # range=[0, 12]
    ),
    font=dict(size=18)
)

# Show figure
fig.show()

# Save the figure as an HTML file
# fig.write_html("MAI090_PercentilesHeatMap.html")
fig.write_json("MAI090_PercentilesHeatMap.json")

# %% -------------------------------------------------------------------

# # Create the figure
# fig = go.Figure()

# # Initialize visibility as False for all traces initially
# all_traces_visibility = {key: False for key in split.keys()}

# # Add traces to the figure for each key in the dictionary
# for key, data in split.items():
#     year, depth = key.split('_')
#     heatmap = go.Heatmap(
#         z=data.values,
#         x=data.columns,
#         y=data.index,
#         colorscale='balance',
#         showscale=False,
#         zmin=-2,
#         zmax=2,
#         visible=True,  # Start as invisible
#         name=f"{year} - {depth}"  # Label each heatmap with year and depth
#     )
#     fig.add_trace(heatmap)

# # Function to update visibility based on year and depth
# def update_visibility(selected_year=None, selected_depth=None):
#     return [all_traces_visibility.get(f"{yr}_{dp}", False)
#             for yr, dp in (key.split('_') for key in split.keys())]

# # Dropdown for Years
# year_buttons = [{
#     "label": year,
#     "method": "update",
#     "args": [{"visible": update_visibility(selected_year=year)}]
# } for year in sorted(set(key.split('_')[0] for key in split.keys()))]

# # Dropdown for Depths
# depth_buttons = [{
#     "label": depth,
#     "method": "update",
#     "args": [{"visible": update_visibility(selected_depth=depth)}]
# } for depth in sorted(set(key.split('_')[1] for key in split.keys()))]

# # Update layout with dual dropdowns
# fig.update_layout(
#     updatemenus=[
#         {"buttons": year_buttons, "direction": "down", "pad": {"r": 10, "t": 10}, "showactive": True,
#          "x": 0.1, "xanchor": "left", "y": 1.2, "yanchor": "top"},
#         {"buttons": depth_buttons, "direction": "down", "pad": {"r": 10, "t": 10}, "showactive": True,
#          "x": 0.3, "xanchor": "left", "y": 1.2, "yanchor": "top"}
#     ],
# )

# # Update layout properties
# fig.update_layout(
#     xaxis=dict(
#         title="Day",
#         tickmode='array',
#         tickvals=list(range(1,len(Tanom0.columns)+1)),  # Ensure every x-tick has a label
#         ticktext=Tanom0.columns,  # Custom text for each tick, matching the column labels
#         tickangle=0,
#         # range=[0, 31]
#     ),
#     yaxis=dict(
#         title="Month",
#         tickmode='array',
#         tickvals=list(range(len(Tanom0.index))),  # Ensure every y-tick has a label
#         ticktext=Tanom0.index,  # Custom text for each tick, matching the index labels
#         # range=[0, 12]
#     ),
#     font=dict(size=18)
# )

# # Update layout properties
# fig.update_layout(
#     xaxis=dict(
#         title="Day",
#         tickmode='array',
#         tickvals=list(range(1,len(Tanom0.columns)+1)),  # Ensure every x-tick has a label
#         ticktext=Tanom0.columns,  # Custom text for each tick, matching the column labels
#         tickangle=0,
#         # range=[0, 31]
#     ),
#     yaxis=dict(
#         title="Month",
#         tickmode='array',
#         tickvals=list(range(len(Tanom0.index))),  # Ensure every y-tick has a label
#         ticktext=Tanom0.index,  # Custom text for each tick, matching the index labels
#         # range=[0, 12]
#     ),
#     font=dict(size=18)
# )

# # Show figure
# fig.show()

# # Save the figure as an HTML file
# fig.write_html("temperature_anomaly.html")


# %%

# # Create heatmap for 10m depth
# heatmap_surf = go.Heatmap(
#     z=Tanom0.values,
#     x=Tanom0.columns,
#     y=Tanom0.index,
#     colorscale='balance',
#     colorbar=None,
#     zmin=-2,zmax=2,
#     showscale=False,   
#     )


# # Create heatmap for 20m depth
# heatmap_21m = go.Heatmap(
#     z=Tanom1.values,
#     x=Tanom1.columns,
#     y=Tanom1.index,
#     colorscale='balance',
#     colorbar=None,
#     zmin=-2,zmax=2,
#     showscale=False
# )

# # Create the figure
# fig = go.Figure()

# # Add the first heatmap (initially shown)
# fig.add_trace(heatmap_surf)

# # Add the second heatmap (initially hidden)
# fig.add_trace(heatmap_21m)

# # Define the update menus (dropdowns)
# fig.update_layout(
#     updatemenus=[
#         {
#             "buttons": [
#                 {
#                     "args": [{"visible": [True, False]}],
#                     "label": "2m Depth",
#                     "method": "update",
#                 },
#                 {
#                     "args": [{"visible": [False, True]}],
#                     "label": "21m Depth",
#                     "method": "update",
#                 },
#             ],
#             "direction": "down",
#             # Increase padding to make the buttons larger
#             "pad": {"r": 10, "t": 10, "l": 10, "b": 10},
#             # Adjust font size to make the text larger
#             "font": {"size": 30},
#             "showactive": True,
#             "x": 0.17,
#             "xanchor": "left",
#             "y": 1.15,
#             "yanchor": "top",
#         },
#     ]
# )

# # Update layout properties
# fig.update_layout(
#     xaxis=dict(
#         title="Day",
#         tickmode='array',
#         tickvals=list(range(1,len(Tanom0.columns)+1)),  # Ensure every x-tick has a label
#         ticktext=Tanom0.columns,  # Custom text for each tick, matching the column labels
#         tickangle=0,
#         # range=[0, 31]
#     ),
#     yaxis=dict(
#         title="Month",
#         tickmode='array',
#         tickvals=list(range(len(Tanom0.index))),  # Ensure every y-tick has a label
#         ticktext=Tanom0.index,  # Custom text for each tick, matching the index labels
#         # range=[0, 12]
#     ),
#     font=dict(size=18)
# )

# # Update the figure layout for a white background and no grid lines
# fig.update_layout(
#     plot_bgcolor='white',  # Set the plot background color to white
#     xaxis=dict(
#         showgrid=False,  # Disable grid lines for the x-axis
#         zeroline=False   # Disable the zero line if needed
#     ),
#     yaxis=dict(
#         showgrid=False,  # Disable grid lines for the y-axis
#         zeroline=False   # Disable the zero line if needed
#     )
# )

# # Update the figure layout to invert the y-axis
# fig.update_layout(
#     yaxis=dict(
#         autorange='reversed'  # Invert the y-axis
#     )
# )

# # Show figure
# fig.show()


# # Save the figure as an HTML file
# fig.write_html("temperature_anomaly.html")

# %% --------------------------------------------------------------------
# convert figure to plotly html

# Step 2: Convert the Matplotlib figure to a Plotly figure
plotly_fig = tls.mpl_to_plotly(plt.gcf())

# Step 3: Save the Plotly figure as an HTML file
pio.write_html(plotly_fig, file='PercentilesHeatMap.html', auto_open=True)

# Show the Matplotlib plot
plt.show()
