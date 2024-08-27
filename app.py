import dash  # type: ignore
from dash import dcc, html  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import plotly.express as px
import pandas as pd

# Suggested name for the web app
app_name = "OceanTemp Visualizer"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.DataFrame({
    "Time": pd.date_range("2021-01-01", periods=100),
    "Temperature": pd.Series(range(100)) + pd.Series(range(100)).apply(lambda x: x ** 0.5)
})

# Enhanced Plotly Plots with Interactivity
fig_line = px.line(
    df, x="Time", y="Temperature", 
    title="Daily Average Temperature",
    color_discrete_sequence=["#FF5733"],
    labels={"Temperature": "Ocean Temperature (°C)", "Time": "Date"},
    template="plotly_dark"
)
fig_line.update_traces(
    mode="markers+lines", 
    marker=dict(size=8, color="#FF5733"),
    hovertemplate="<b>Date</b>: %{x}<br><b>Temperature</b>: %{y}°C<extra></extra>"
)

fig_scatter = px.scatter(
    df, x="Time", y="Temperature", 
    title="Scatter Plot of Temperature",
    color="Temperature", 
    color_continuous_scale=px.colors.sequential.Viridis,
    labels={"Temperature": "Ocean Temperature (°C)", "Time": "Date"},
    template="plotly_dark"
)
fig_scatter.update_traces(
    marker=dict(size=12, opacity=0.8, line=dict(width=2, color='DarkSlateGrey')),
    hovertemplate="<b>Date</b>: %{x}<br><b>Temperature</b>: %{y}°C<extra></extra>"
)

fig_bar = px.bar(
    df, x="Time", y="Temperature", 
    title="Temperature Bar Chart",
    color="Temperature",
    color_continuous_scale=px.colors.sequential.Bluered,
    labels={"Temperature": "Ocean Temperature (°C)", "Time": "Date"},
    template="plotly_dark"
)
fig_bar.update_traces(
    hovertemplate="<b>Date</b>: %{x}<br><b>Temperature</b>: %{y}°C<extra></extra>",
    marker=dict(line=dict(color='DarkSlateGrey', width=1.5))
)

# Define the layout of the app
app.layout = html.Div(style={'backgroundColor': '#f8f9fa'}, children=[
    
    # Header with Wave Design and Logo
    html.Header([
        html.Div([
            html.Img(src="/assets/ocean-heatwave-logo.jfif", className="logo"),
            html.Div([
                html.H1(app_name, style={'margin-bottom': '0px'}),
                html.H4("Visualizing the changing temperatures of our oceans", style={'margin-top': '0px'}),
            ], className="header-text"),
        ], className="header-content"),
        html.Nav([
            html.A("Home", href="#", className="nav-link"),
            html.A("About", href="#", className="nav-link"),
            html.A("Visualizations", href="#visualizations", className="nav-link"),  # New Visualizations link
            html.A("Contact", href="#", className="nav-link"),
        ], className="nav-bar")
    ], className="header"),
    
    # Introductory Section with Faded Background Image on the Right
    html.Section([
        html.Div([
            html.H2(f"Welcome to {app_name}!"),
            html.P("Explore the visualizations of ocean temperature data and learn about how our oceans are heating up."),
            html.P("Red indicates intense heatwaves, while blue shows cooler regions. Dive into the data below!"),
        ], className="intro-text"),
        html.Img(src="/assets/marine-ecosystem-2.jfif", className="intro-graphic")
    ], className="intro-section", style={"display": "flex", "justify-content": "space-between", "align-items": "center"}),

    # Visualizations Section
    html.Section(id="visualizations", children=[
        # Daily Average Temperature Section
        html.Div([
            html.H2("Daily Average Temperature"),
            html.H4("Overview"),
            html.P("This section visualizes the daily average temperature of the ocean, helping in understanding the overall trend of temperature changes over time."),
            dcc.Graph(
                id='line-chart',
                figure=fig_line
            ),
        ], className="plot-section", style={"backgroundImage": "url('/assets/image.png')", "backgroundSize": "cover", "padding": "50px", "borderRadius": "15px", "marginBottom": "40px"}),

        # Scatter Plot Section
        html.Div([
            html.H2("Scatter Plot of Temperature"),
            html.H4("Detailed View"),
            html.P("This section shows a scatter plot of temperature data points over time, highlighting potential outliers or anomalies."),
            dcc.Graph(
                id='scatter-plot',
                figure=fig_scatter
            ),
        ], className="plot-section", style={"backgroundImage": "url('/assets/image.png')", "backgroundSize": "cover", "padding": "50px", "borderRadius": "15px", "marginBottom": "40px"}),

        # Bar Chart Section
        html.Div([
            html.H2("Temperature Bar Chart"),
            html.H4("Comparative Analysis"),
            html.P("This bar chart provides a comparative analysis of temperature distributions over time."),
            dcc.Graph(
                id='bar-chart',
                figure=fig_bar
            ),
        ], className="plot-section", style={"backgroundImage": "url('/assets/image.png')", "backgroundSize": "cover", "padding": "50px", "borderRadius": "15px", "marginBottom": "40px"}),
    ], className="content"),
    
    # Footer with Wave Design
    html.Footer([
        html.Div([
            html.P(f"© 2024 {app_name}"),
            html.P("Disclaimer: The data and information presented on this dashboard are provided for informational purposes only. "
                   "While every effort has been made to ensure the accuracy of the data, users should verify information before relying on it. "
                   f"{app_name} and its affiliates do not accept any responsibility for any loss or damage caused by use of the information contained herein."),
        ], className="footer-content"),
        html.Div([
            html.A("Privacy Policy", href="#", className="footer-link"),
            html.Span(" | ", className="footer-separator"),
            html.A("Terms of Service", href="#", className="footer-link"),
        ], className="footer-links")
    ], className="footer")
])

# Internal custom CSS and JavaScript for wave effects
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>''' + app_name + '''</title>
        <link rel="icon" href="/assets/favicon.jfif" type="image/x-icon">  <!-- Updated favicon link -->
        {%css%}
        <style>
            body {
                background-color: #f8f9fa;
                color: #333333;
                font-family: Arial, sans-serif;
            }

            .header {
                background: linear-gradient(180deg, #27B5C1, #1897A6, #118093, #0B657D); /* Gradient with specified colors */
                color: white;
                padding: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: relative;
                z-index: 10;
            }

            .header::after {
                content: "";
                display: block;
                width: 100%;
                height: 100px;
                background-image: url('/assets/image.png'); /* Add the wave design image */
                background-size: cover;
                position: absolute;
                bottom: -50px; /* Adjust to make the wave part of the header */
                left: 0;
                right: 0;
                z-index: 5;
            }

            .header-content {
                display: flex;
                align-items: center;
                z-index: 10;
            }

            .logo {
                margin-right: 20px;
                height: 80px; /* Adjust the height to make the logo fit well */
                border-radius: 15px; /* Apply some rounding to integrate better with the header */
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5); /* Add a slight shadow for depth */
            }

            .header-text h1, .header-text h4 {
                margin: 0;
            }

            .nav-bar {
                display: flex;
                gap: 20px;
                z-index: 10;
            }

            .nav-link {
                color: white;
                text-decoration: none;
            }

            .nav-link:hover {
                text-decoration: underline;
            }

            .intro-section {
                height: 600px;
                padding: 40px 20px;
                display: flex;
                align-items: center;
                color: white;
                position: relative;
                z-index: 1;
                overflow: hidden;
                background: linear-gradient(120deg, #002040 0%, #006080 50%, #004080 100%);
            }

            .intro-text {
                max-width: 50%;
                z-index: 2;
            }

            .intro-graphic {
                max-width: 60%;
                opacity: 0.2; /* Fading the image for subtle background effect */
                position: absolute;
                right: 0;
                bottom: 0;
                z-index: 1;
            }

            .content {
                padding: 20px;
                margin-top: 40px;
            }

            .plot-section {
                margin-bottom: 40px;
                background-color: rgba(0, 31, 63, 0.8); /* Slightly transparent background */
                color: white;
                padding: 20px;
                border-radius: 15px;
                position: relative;
                background-size: cover;
            }

            .footer {
                background-color: #002040;
                color: white;
                padding: 20px;
                text-align: center;
                margin-top: 40px;
                position: relative;
            }

            .footer::before {
                content: "";
                display: block;
                width: 100%;
                height: 100px;
                background-image: url('/assets/image.png'); /* Add the wave design image */
                background-size: cover;
                position: absolute;
                top: -50px; /* Adjust to make the wave part of the footer */
                left: 0;
                right: 0;
                z-index: 5;
            }

            .footer-content {
                margin-bottom: 20px;
                z-index: 10;
                position: relative;
            }

            .footer-links {
                margin-top: 10px;
                z-index: 10;
                position: relative;
            }

            .footer-link {
                color: white;
                text-decoration: none;
                margin-right: 10px;
            }

            .footer-link:hover {
                text-decoration: underline;
            }

            .footer-separator {
                margin-right: 10px;
                color: #ffffff;
            }

            /* Adding Ocean Animation */
            @keyframes oceanWaves {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            .intro-section::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: url('/assets/marine-ecosystem-2.jfif');
                background-size: contain;
                background-repeat: no-repeat;
                background-position: right bottom;
                opacity: 0.1; /* Faded background */
                z-index: 1;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run_server(debug=True)
