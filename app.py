import dash  # type: ignore
from dash import dcc, html, Input, Output, State  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import plotly.io as pio
import json
import time
from flask_caching import Cache
import threading  # <-- Make sure this is imported
import subprocess
import dash_html_components as html

script_path = "AWS-SES-SendAcknowledgement.py"


# Function to load the HTML file content
def load_html_content(file_path):
    with open(file_path, "r") as f:
        return f.read()


# Function to run the two scripts
def run_scripts():
    while True:
        # Run CheckJson.py
        subprocess.run(["python", "CheckJson.py"])
        # Run CheckRecord.py
        subprocess.run(["python", "CheckRecord.py"])
        # Wait for 2 minutes before running again
        time.sleep(600)


# Start the background task
script_thread = threading.Thread(target=run_scripts, daemon=True)
script_thread.start()


# Suggested name for the web app
app_name = "MessageMeWhenItsHot"

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,  # Bootstrap CSS
        "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css",  # Animate.css for animations
    ],
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/js/all.min.js",  # FontAwesome
        "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js",  # jQuery
        "/assets/custom.js",
    ],
    suppress_callback_exceptions=True,
)

# Setup Flask-Caching
cache = Cache(
    app.server,
    config={
        "CACHE_TYPE": "simple",
        "CACHE_DEFAULT_TIMEOUT": 300,
    },
)


# Function to load and fix JSON files
def load_and_fix_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    # Validate and correct color fields
    for trace in data.get("data", []):
        if "marker" in trace:
            if "color" in trace["marker"]:
                if isinstance(trace["marker"]["color"], list):
                    trace["marker"]["color"] = [
                        (
                            color if isinstance(color, str) else "#000000"
                        )  # Default to black if invalid
                        for color in trace["marker"]["color"]
                    ]
                elif not isinstance(trace["marker"]["color"], str):
                    trace["marker"]["color"] = "#000000"  # Default to black if invalid
    fig = pio.from_json(json.dumps(data))
    return fig


# Introductory page layout

intro_layout = html.Div(
    style={
        "background-image": "url('/assets/Gemini_Generated_Image_zbsammzbsammzbsa.jfif')",
        "background-size": "cover",
        "background-position": "center",
        "background-repeat": "no-repeat",
        "height": "100vh",
        "position": "relative",
        "overflow": "hidden",
    },
    children=[
        html.Div(
            style={
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "background-color": "rgba(255, 255, 255, 0.7)",
                "z-index": "1",
            }
        ),
        html.Div(
            [
                html.Img(
                    src="/assets/message-me-logo.jfif",
                    style={
                        "display": "block",
                        "margin": "0 auto",
                        "width": "150px",
                        "height": "150px",
                        "margin-bottom": "20px",
                    },
                ),
                html.H1(
                    "MessageMeWhenItsHot",
                    style={
                        "font-size": "64px",
                        "color": "darkblue",
                        "text-align": "center",
                        "font-weight": "bold",
                        "margin-bottom": "20px",
                    },
                ),
                html.H2(
                    "A web app to visualize ocean temperatures and send alerts to subscribed users when temperatures rise.",
                    style={
                        "font-size": "36px",
                        "color": "darkblue",
                        "text-align": "center",
                        "margin-bottom": "20px",
                    },
                ),
                html.P(
                    "MessageMeWhenItsHot allows users to explore subsurface ocean extremes at coastal locations around Australia. Users are also able to sign up to receive notifications when new data is available and whether or not a temperature record has been broken. It was inspired by the website https://isithotrightnow.com/ and was developed during Ocean Hackweek 2024.",
                    style={
                        "font-size": "24px",
                        "color": "darkblue",
                        "text-align": "center",
                        "margin-bottom": "40px",
                    },
                ),
                # Collaborators section
                html.Div(
                    [
                        html.H3(
                            "Collaborators",
                            style={
                                "font-size": "48px",
                                "color": "darkblue",
                                "text-align": "left",
                                "margin-bottom": "20px",
                            },
                        ),
                        html.Ul(
                            [
                                html.Li(
                                    "Michael Hemming",
                                    style={"font-size": "36px", "color": "darkblue"},
                                ),
                                html.Li(
                                    "Natalia Ribeiro",
                                    style={"font-size": "36px", "color": "darkblue"},
                                ),
                                html.Li(
                                    "Ranisa Gupta",
                                    style={"font-size": "36px", "color": "darkblue"},
                                ),
                                html.Li(
                                    "Toan Bui",
                                    style={"font-size": "36px", "color": "darkblue"},
                                ),
                                html.Li(
                                    "Jun Yu",
                                    style={"font-size": "36px", "color": "darkblue"},
                                ),
                                html.Li(
                                    "Ben Stepin",
                                    style={"font-size": "36px", "color": "darkblue"},
                                ),
                            ],
                            style={
                                "list-style-type": "disc",
                                "padding-left": "20px",
                                "font-weight": "bold",
                                "text-align": "left",
                            },
                        ),
                    ],
                    style={
                        "position": "relative",
                        "top": "0",
                        "left": "0",
                        "text-align": "left",
                        "z-index": "2",
                        "padding-left": "10px",
                    },
                ),
            ],
            style={
                "position": "absolute",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "text-align": "center",
                "z-index": "2",
                "width": "80%",
            },
        ),
    ],
)


# Video cover section with blur overlay and search bar
video_cover_section = html.Section(
    [
        html.Div(
            [
                # Background Video
                html.Video(
                    src="/assets/webapp-cover-video.mov",
                    autoPlay=True,
                    loop=True,
                    muted=True,
                    style={
                        "width": "100%",
                        "height": "100%",
                        "object-fit": "cover",
                        "position": "absolute",
                        "top": "0",
                        "left": "0",
                        "z-index": "1",
                    },
                ),
                # Updated Ocean Blue Overlay
                html.Div(
                    style={
                        "position": "absolute",
                        "top": "0",
                        "left": "0",
                        "right": "0",
                        "bottom": "0",
                        "background-color": "rgba(86, 154, 160, 0.39)",  # Updated overlay color
                        "z-index": "2",
                        "backdrop-filter": "blur(8px)",
                    }
                ),
                # Subheading, Lines, and Search Bar Content
                html.Div(
                    [
                        # Subheading
                        html.H1(
                            "Is it hot in Maria Island right now?",
                            style={
                                "font-size": "36px",
                                "color": "red",
                                "text-align": "center",
                                "margin-bottom": "20px",
                                "font-weight": "bold",
                                "margin-top": "3em",
                                "margin-bottom": "3em",
                            },
                        ),
                        # Temperature and Trend Information
                        html.Div(
                            [
                                # Latest Temperature
                                html.Div(
                                    [
                                        html.I(
                                            className="fas fa-thermometer-half",
                                            style={
                                                "color": "orange",
                                                "font-size": "36px",
                                                "margin-right": "10px",
                                                "vertical-align": "middle",
                                            },
                                        ),
                                        html.Span(
                                            "Maria Island Latest Temperature: 13.2°C",
                                            style={
                                                "font-size": "28px",
                                                "color": "orange",
                                                "font-weight": "bold",
                                                "vertical-align": "middle",
                                            },
                                        ),
                                    ],
                                    style={
                                        "text-align": "center",
                                        "margin-bottom": "10px",
                                    },
                                ),
                                # Temperature Trend
                                html.Div(
                                    [
                                        html.I(
                                            className="fas fa-chart-line",
                                            style={
                                                "color": "orange",
                                                "font-size": "36px",
                                                "margin-right": "10px",
                                                "vertical-align": "middle",
                                            },
                                        ),
                                        html.Span(
                                            "Trend: 0.018°C per year",
                                            style={
                                                "font-size": "28px",
                                                "color": "orange",
                                                "font-weight": "bold",
                                                "vertical-align": "middle",
                                            },
                                        ),
                                    ],
                                    style={
                                        "text-align": "center",
                                        "margin-bottom": "30px",
                                    },
                                ),
                            ],
                            style={
                                "position": "relative",
                                "z-index": "3",
                                "margin-bottom": "30px",  # Adjust margin to create spacing
                            },
                        ),
                        # Temperature status
                        # html.Div(
                        #     [
                        #         html.Span(
                        #             className="fas fa-circle",
                        #             style={
                        #                 "color": "red",
                        #                 "font-size": "36px",
                        #                 "margin-right": "15px",
                        #                 "vertical-align": "middle",
                        #             },
                        #         ),
                        #         html.Span(
                        #             "Hell yeah!",
                        #             style={
                        #                 "font-size": "48px",
                        #                 "color": "white",
                        #                 "font-weight": "bold",
                        #                 "vertical-align": "middle",
                        #             },
                        #         ),
                        #     ],
                        #     style={"text-align": "center", "margin-bottom": "20px"},
                        # ),
                        # Search Bar
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Input(
                                            id="location-search",
                                            value="Maria Island",
                                            type="text",
                                            disabled=True,
                                            style={
                                                "font-size": "22px",
                                                "padding": "15px 30px",
                                                "border-radius": "25px",
                                                "width": "100%",
                                                "font-weight": "600",
                                                "font-style": "italic",
                                                "border": "none",
                                                "outline": "none",
                                                "box-shadow": "none",
                                                "background-color": "transparent",
                                                "color": "darkred",  # Text color
                                            },
                                            className="typed-text",
                                        ),
                                        html.I(
                                            className="fas fa-map-marker-alt",
                                            style={
                                                "font-size": "24px",
                                                "color": "darkblue",
                                                "margin-left": "20px",
                                                "vertical-align": "middle",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                        "justify-content": "space-between",
                                        "background-color": "rgba(255, 255, 255, 0.8)",
                                        "border-radius": "25px",
                                        "width": "100%",
                                        "transition": "box-shadow 0.3s ease-in-out, border-color 0.3s ease-in-out",
                                        "border": "4px solid transparent",
                                        "margin-bottom": "2em",
                                    },
                                    className="search-bar",
                                ),
                            ],
                            style={
                                "width": "42%",
                                "margin": "0 auto",
                                "text-align": "center",
                                "position": "relative",
                                "z-index": "3",
                                "margin-top": "5em",
                            },
                        ),
                        # Arrow Down to Visualizations
                        html.Div(
                            [
                                html.A(
                                    href="#visualizations",
                                    children=html.I(
                                        className="fas fa-arrow-down",
                                        style={
                                            "font-size": "42px",
                                            "color": "white",
                                            "margin-top": "180px",
                                        },
                                    ),
                                ),
                            ],
                            style={
                                "text-align": "center",
                                "position": "relative",
                                "z-index": "3",
                                "margin-top": "4em",
                            },
                        ),
                    ],
                    style={"position": "relative", "z-index": "3"},
                ),
            ],
            style={"position": "relative", "height": "100vh", "overflow": "hidden"},
        )
    ]
)


# Main app layout
main_layout = html.Div(
    style={"backgroundColor": "#f8f9fa"},
    children=[
        html.Header(
            [
                html.Div(
                    [
                        html.A(
                            href="/home",
                            children=[
                                html.Img(
                                    src="/assets/Gemini_Generated_Image_67twfk67twfk67tw.jfif",
                                    className="logo",
                                    style={
                                        "height": "120px",
                                        "margin-right": "15px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.H1(
                                            app_name,
                                            style={
                                                "margin-bottom": "0px",
                                                "font-size": "36px",
                                                "font-weight": "700",
                                                "color": "Lightgrey",
                                            },
                                        ),
                                    ],
                                    className="header-text",
                                ),
                            ],
                            style={
                                "display": "flex",
                                "align-items": "center",
                                "text-decoration": "none",
                            },
                        ),
                    ],
                    className="header-content",
                ),
                html.Nav(
                    [
                        html.A("Home", href="#home", className="nav-link"),
                        html.A(
                            "Visualizations",
                            href="#visualizations",
                            className="nav-link",
                        ),
                        html.A("About", href="#about", className="nav-link"),
                        html.A("Contact", href="#contact", className="nav-link"),
                    ],
                    className="nav-bar",
                    style={"margin-left": "auto"},  # Align nav items to the right
                ),
                html.Div(
                    [
                        html.A(
                            [
                                html.I(
                                    className="fas fa-bell",
                                    style={"color": "red", "margin-right": "10px"},
                                ),
                                "SIGN UP",
                            ],
                            href="/signup",
                            className="sign-up-btn",
                        )
                    ],
                    style={"text-align": "right", "padding-right": "20px"},
                ),
            ],
            className="header",
            id="home",
        ),
        # Add the video cover section before the visualization section
        video_cover_section,
        # Visualization Section Header
        html.Section(
            [
                html.Div(
                    [
                        html.H3(
                            "Visualizations",
                            style={
                                "font-size": "44px",
                                "color": "#172427",
                                "text-align": "center",
                                "font-weight": "700",
                            },
                        ),
                        html.P(
                            "Explore detailed visual representations of ocean temperature data and learn about how temperature fluctuations affect marine ecosystems.",
                            style={
                                "font-size": "22px",
                                "color": "#666666",
                                "text-align": "center",
                                "padding": "20px",
                            },
                        ),
                    ],
                    style={"padding": "40px 0"},
                )
            ],
            id="visualizations",
        ),
        html.Main(
            [
                # In your layout
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-chart-bar"),
                                "Maria Island Daily Average Temperature Plot ",
                            ],
                            style={
                                "font-size": "34px",
                                "color": "#006080",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-info-circle"),
                                " This plot shows the daily average ocean temperatures, providing insights into temperature trends over time.",
                            ],
                            style={
                                "font-size": "20px",
                                "color": "#004080",
                                "text-align": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        html.Div(
                            [
                                html.Iframe(
                                    srcDoc=load_html_content(
                                        "Figures/DailyAVG_plot.html"
                                    ),  # Load the HTML content without heading
                                    style={
                                        "width": "90%",  # Center the plot by adjusting the width
                                        "height": "600px",  # Adjust the height as needed
                                        "border": "none",
                                        "margin": "0 auto",  # Center the iframe horizontally
                                        "display": "block",
                                    },
                                )
                            ],
                            style={"text-align": "center", "margin-top": "20px"},
                        ),
                    ],
                    className="plot-section",
                    style={"padding": "20px", "margin": "60px 0"},
                ),
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-thermometer-half"),
                                " Ocean Temperature Anomalies Heat Map",
                            ],
                            style={
                                "font-size": "34px",
                                "color": "#006080",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-info-circle"),
                                " This heat map provides a visual representation of ocean temperature percentiles, helping to identify patterns and anomalies in temperature changes across different regions. The data is crucial for understanding the impact of temperature fluctuations on marine ecosystems.",
                            ],
                            style={
                                "font-size": "20px",
                                "color": "#004080",
                                "text-align": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        dcc.Loading(
                            id="loading-2",
                            type="default",
                            children=dcc.Graph(id="heatmap-graph"),
                        ),
                    ],
                    className="plot-section",
                    style={"padding": "20px", "margin": "60px 0"},
                ),
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-chart-line"),
                                " Marine Heatwaves Per Time (Temperature Anomaly) Heatmap",
                            ],
                            style={
                                "font-size": "34px",
                                "color": "#006080",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-info-circle"),
                                " This heat map shows marine heatwaves over time and corresponding temperature anomalies.",
                            ],
                            style={
                                "font-size": "20px",
                                "color": "#004080",
                                "text-align": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        dcc.Loading(
                            id="loading-temp-anom",
                            type="default",
                            children=dcc.Graph(id="temp-anom-heatmap-graph"),
                        ),
                    ],
                    className="plot-section",
                    style={"padding": "20px", "margin": "60px 0"},
                ),
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-water"),
                                " Temperature Distribution Plot (MAI 2m) ",
                                html.Span(
                                    "2m",
                                    style={
                                        "color": "orange",
                                        "font-weight": "bold",
                                        "margin-left": "10px",
                                    },
                                ),
                            ],
                            style={
                                "font-size": "34px",
                                "color": "#006080",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-info-circle"),
                                " This plot represents the temperature distribution at 2 meters depth for the MAI location. The plot is essential for tracking temperature changes at shallow depths and analyzing their effects on coastal marine life.",
                            ],
                            style={
                                "font-size": "20px",
                                "color": "#004080",
                                "text-align": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        dcc.Loading(
                            id="loading-3",
                            type="default",
                            children=dcc.Graph(id="temp-dist-plot-graph"),
                        ),
                    ],
                    className="plot-section",
                    style={"padding": "20px", "margin": "60px 0"},
                ),
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-water"),
                                " Temperature Distribution Plot (MAI 21m) ",
                                html.Span(
                                    "21m",
                                    style={
                                        "color": "orange",
                                        "font-weight": "bold",
                                        "margin-left": "10px",
                                    },
                                ),
                            ],
                            style={
                                "font-size": "34px",
                                "color": "#006080",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-info-circle"),
                                " This plot represents the temperature distribution at 21 meters depth for the MAI location. It offers insights into temperature variations at greater depths, which are critical for understanding deep-water ecosystems.",
                            ],
                            style={
                                "font-size": "20px",
                                "color": "#004080",
                                "text-align": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        dcc.Loading(
                            id="loading-4",
                            type="default",
                            children=dcc.Graph(id="temp-dist-plot-graph-21m"),
                        ),
                    ],
                    className="plot-section",
                    style={"padding": "20px", "margin": "60px 0"},
                ),
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-cloud-rain"),
                                " Rainfall Heat Map",
                                html.Span(
                                    "Rainfall Data",
                                    style={
                                        "color": "blue",
                                        "font-weight": "bold",
                                        "margin-left": "10px",
                                    },
                                ),
                            ],
                            style={
                                "font-size": "34px",
                                "color": "#006080",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-info-circle"),
                                " This heat map visualizes the distribution of rainfall over various regions. It is crucial for understanding the impact of rainfall on marine ecosystems.",
                            ],
                            style={
                                "font-size": "20px",
                                "color": "#004080",
                                "text-align": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        dcc.Loading(
                            id="loading-6",
                            type="default",
                            children=dcc.Graph(id="rainfall-heatmap-graph"),
                        ),
                    ],
                    className="plot-section",
                    style={"padding": "20px", "margin": "60px 0"},
                ),
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-chart-bar"),
                                " Accumulated Temperature Plot for 2024",
                            ],
                            style={
                                "font-size": "34px",
                                "color": "#006080",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-info-circle"),
                                " This plot shows the accumulated ocean temperature data for 2024.",
                            ],
                            style={
                                "font-size": "20px",
                                "color": "#004080",
                                "text-align": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        dcc.Loading(
                            id="loading-acumulada",
                            type="default",
                            children=dcc.Graph(id="acumulada-plot-graph"),
                        ),
                    ],
                    className="plot-section",
                    style={"padding": "20px", "margin": "60px 0"},
                ),
                # Add this section in the appropriate place within your visualizations section
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-chart-line"),
                                " Accumulated Temperature Plot for August 2024",
                            ],
                            style={
                                "font-size": "34px",
                                "color": "#006080",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-info-circle"),
                                " This plot represents the accumulated ocean temperature data for August 2024, providing insights into temperature accumulation patterns.",
                            ],
                            style={
                                "font-size": "20px",
                                "color": "#004080",
                                "text-align": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        dcc.Loading(
                            id="loading-acumulada-aug",
                            type="default",
                            children=dcc.Graph(id="acumulada-aug-plot-graph"),
                        ),
                    ],
                    className="plot-section",
                    style={"padding": "20px", "margin": "60px 0"},
                ),
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-temperature-high"),
                                " Marine Heatwaves Per Time Heat Map",
                                html.Span(
                                    "MHW Data",
                                    style={
                                        "color": "red",
                                        "font-weight": "bold",
                                        "margin-left": "10px",
                                    },
                                ),
                            ],
                            style={
                                "font-size": "34px",
                                "color": "#006080",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-info-circle"),
                                " This heat map shows the occurrences of marine heatwaves over time. Understanding these patterns is vital for predicting future events and protecting marine life.",
                            ],
                            style={
                                "font-size": "20px",
                                "color": "#004080",
                                "text-align": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        dcc.Loading(
                            id="loading-7",
                            type="default",
                            children=dcc.Graph(id="mhw-heatmap-graph"),
                        ),
                    ],
                    className="plot-section",
                    style={"padding": "20px", "margin": "60px 0"},
                ),
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-chart-line"),
                                " Daily Spike in Ocean Temperature",
                            ],
                            style={
                                "font-size": "34px",
                                "color": "#006080",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.P(
                            [
                                html.I(className="fas fa-info-circle"),
                                " This plot shows the daily spikes in ocean temperatures, providing insights into rapid changes in temperature over short periods.",
                            ],
                            style={
                                "font-size": "20px",
                                "color": "#004080",
                                "text-align": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        dcc.Loading(
                            id="loading-8",  # Unique ID for loading spinner
                            type="default",
                            children=dcc.Graph(
                                id="daily-spike-graph"
                            ),  # ID for the new plot
                        ),
                    ],
                    className="plot-section",
                    style={"padding": "20px", "margin": "60px 0"},
                ),
            ],
            className="content",
        ),
        # About Us Section
        html.Section(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.I(
                                            className="fas fa-info-circle",
                                            style={
                                                "font-size": "50px",
                                                "color": "#FF5733",
                                                "margin-right": "10px",
                                            },
                                        ),
                                        html.H3(
                                            "About Us",
                                            style={
                                                "font-size": "36px",
                                                "color": "#333333",
                                                "font-weight": "bold",
                                                "margin-bottom": "0px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                        "justify-content": "center",
                                        "margin-bottom": "20px",
                                    },
                                ),
                                html.Hr(
                                    style={
                                        "border": "1px solid #333333",
                                        "width": "80%",
                                        "margin": "0 auto",
                                        "margin-bottom": "20px",
                                    }
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Img(
                                                    src="/assets/message-me-logo.jfif",
                                                    style={
                                                        "height": "80px",
                                                        "vertical-align": "middle",
                                                        "margin-right": "20px",
                                                    },
                                                ),
                                                html.Span(
                                                    "MessageMeWhenItsHot",
                                                    style={
                                                        "font-size": "36px",
                                                        "color": "#FF5733",
                                                        "font-weight": "bold",
                                                        "vertical-align": "middle",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "align-items": "center",
                                                "justify-content": "center",
                                                "margin-bottom": "20px",
                                            },
                                        ),
                                        html.H4(
                                            "Explore subsurface ocean extremes at coastal locations around Australia.",
                                            style={
                                                "font-size": "28px",
                                                "color": "#333333",
                                                "text-align": "center",
                                                "margin-bottom": "20px",
                                                "font-weight": "normal",
                                            },
                                        ),
                                        html.P(
                                            [
                                                "MessageMeWhenItsHot allows users to explore subsurface ocean extremes at coastal locations around Australia. ",
                                                "Users are also able to sign up to receive notifications when new data is available and whether or not a temperature record has been broken.",
                                                html.Br(),
                                                html.Br(),
                                                html.I(
                                                    className="fas fa-lightbulb",
                                                    style={
                                                        "color": "#FF5733",
                                                        "margin-right": "10px",
                                                        "font-size": "20px",
                                                    },
                                                ),
                                                "It was inspired by the website ",
                                                html.A(
                                                    "Is it Hot Right Now?",
                                                    href="https://isithotrightnow.com/",
                                                    style={
                                                        "color": "#0056b3",
                                                        "text-decoration": "underline",
                                                    },
                                                ),
                                                " and was developed during Ocean Hackweek 2024.",
                                                html.Br(),
                                                html.Br(),
                                                html.I(
                                                    className="fas fa-users",
                                                    style={
                                                        "color": "#FF5733",
                                                        "margin-right": "10px",
                                                        "font-size": "20px",
                                                    },
                                                ),
                                                html.Strong("Contributors: "),
                                                html.Span(
                                                    "Ben Stepin, ",
                                                    style={
                                                        "color": "#004080",
                                                        "font-weight": "bold",
                                                    },
                                                ),
                                                html.Span(
                                                    "Jun Yu, ",
                                                    style={
                                                        "color": "#004080",
                                                        "font-weight": "bold",
                                                    },
                                                ),
                                                html.Span(
                                                    "Michael Hemming, ",
                                                    style={
                                                        "color": "#004080",
                                                        "font-weight": "bold",
                                                    },
                                                ),
                                                html.Span(
                                                    "Natalia Ribeiro, ",
                                                    style={
                                                        "color": "#004080",
                                                        "font-weight": "bold",
                                                    },
                                                ),
                                                html.Span(
                                                    "Ranisa Gupta, ",
                                                    style={
                                                        "color": "#004080",
                                                        "font-weight": "bold",
                                                    },
                                                ),
                                                html.Span(
                                                    "Toan Bui",
                                                    style={
                                                        "color": "#004080",
                                                        "font-weight": "bold",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "font-size": "20px",
                                                "color": "#555555",
                                                "text-align": "left",
                                                "line-height": "1.6",
                                                "max-width": "800px",
                                                "margin": "0 auto",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "60px 20px",
                                        "backgroundColor": "rgb(57 198 210 / 19%)",
                                        "border-radius": "10px",
                                        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                        "margin-bottom": "60px",
                                    },
                                ),
                            ]
                        ),
                    ],
                    id="about",
                ),
            ]
        ),
        # Contact Us Section
        # Contact Us Section
        html.Section(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.I(
                                            className="fas fa-phone-alt",
                                            style={
                                                "font-size": "50px",
                                                "color": "#FF5733",
                                                "margin-right": "10px",
                                            },
                                        ),
                                        html.H3(
                                            "Contact Us",
                                            style={
                                                "font-size": "36px",
                                                "color": "#333333",
                                                "font-weight": "bold",
                                                "margin-bottom": "0px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                        "justify-content": "center",
                                        "margin-bottom": "20px",
                                    },
                                ),
                                html.Hr(
                                    style={
                                        "border": "1px solid #333333",
                                        "width": "80%",
                                        "margin": "0 auto",
                                        "margin-bottom": "20px",
                                    }
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            [
                                                html.I(
                                                    className="fas fa-envelope",
                                                    style={
                                                        "color": "#FF5733",
                                                        "margin-right": "10px",
                                                    },
                                                ),
                                                "You can contact the web app team via email: ",
                                                html.A(
                                                    "messagemewhenitshot@gmail.com",
                                                    href="mailto:messagemewhenitshot@gmail.com",
                                                    style={
                                                        "color": "#0056b3",
                                                        "text-decoration": "underline",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "font-size": "20px",
                                                "color": "#555555",
                                                "line-height": "1.6",
                                                "margin-bottom": "20px",
                                                "font-weight": "bold",
                                                "color": "#004080",
                                                "text-align": "center",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.I(
                                                            className="fas fa-mail-bulk",
                                                            style={
                                                                "color": "#FFC300",
                                                                "margin-right": "10px",
                                                                "font-size": "20px",
                                                            },
                                                        ),
                                                        html.Span(
                                                            "MMWIH HQ",
                                                            style={
                                                                "color": "#004080",
                                                                "font-weight": "bold",
                                                                "font-size": "22px",
                                                            },
                                                        ),
                                                        html.Br(),
                                                        html.Span(
                                                            "Kioloa ANU Coastal Campus,",
                                                            style={"color": "#555555"},
                                                        ),
                                                        html.Br(),
                                                        html.Span(
                                                            "496 Murramarang Rd,",
                                                            style={"color": "#555555"},
                                                        ),
                                                        html.Br(),
                                                        html.Span(
                                                            "Kioloa NSW 2539",
                                                            style={"color": "#555555"},
                                                        ),
                                                    ],
                                                    style={
                                                        "padding": "20px",
                                                        "backgroundColor": "#f9f9f9",
                                                        "border-radius": "10px",
                                                        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                                        "margin-bottom": "20px",
                                                    },
                                                ),
                                                html.Div(
                                                    [
                                                        html.I(
                                                            className="fas fa-map-marker-alt",
                                                            style={
                                                                "color": "#FF5733",
                                                                "margin-right": "10px",
                                                                "font-size": "20px",
                                                            },
                                                        ),
                                                        html.Span(
                                                            "MMWIH Innovation Hub",
                                                            style={
                                                                "color": "#004080",
                                                                "font-weight": "bold",
                                                                "font-size": "22px",
                                                            },
                                                        ),
                                                        html.Br(),
                                                        html.Span(
                                                            "Pebbly Beach,",
                                                            style={"color": "#555555"},
                                                        ),
                                                        html.Br(),
                                                        html.Span(
                                                            "NSW 2536",
                                                            style={"color": "#555555"},
                                                        ),
                                                    ],
                                                    style={
                                                        "padding": "20px",
                                                        "backgroundColor": "#f9f9f9",
                                                        "border-radius": "10px",
                                                        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "max-width": "600px",
                                                "margin": "0 auto",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "60px 20px",
                                        "backgroundColor": "rgb(57 198 210 / 19%)",
                                        "border-radius": "10px",
                                        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                    },
                                ),
                            ]
                        ),
                    ],
                    id="contact",
                ),
            ]
        ),
        # New footer section with IMOS acknowledgment
        html.Footer(
            [
                html.Div(
                    className="d-flex justify-content-between align-items-center",
                    style={
                        "padding": "10px 20px",  # Adjust padding as needed
                        "height": "100px",  # Adjust height as needed
                    },
                    children=[
                        # IMOS logo on the far left
                        html.Div(
                            html.Img(
                                src="/assets/footer-logo.png", style={"height": "75px"}
                            ),
                            style={"flex": "0 0 auto"},  # Fixed width for logo div
                        ),
                        # Acknowledgment content centered
                        html.Div(
                            [
                                html.P(
                                    "Data were sourced from Australia’s Integrated Marine Observing System (IMOS) – IMOS is enabled by the National Collaborative Research Infrastructure Strategy (NCRIS).",
                                    style={
                                        "font-size": "17px",  # Adjust font size as needed
                                        "color": "white",
                                        "margin-bottom": "0",
                                        "font-weight": "500",
                                    },
                                ),
                                html.P(
                                    "It is operated by a consortium of institutions as an unincorporated joint venture, with the University of Tasmania as Lead Agent.",
                                    style={
                                        "font-size": "17px",  # Adjust font size as needed
                                        "color": "white",
                                        "margin-bottom": "0",
                                        "font-weight": "500",
                                    },
                                ),
                                html.A(
                                    "Acknowledgements",
                                    href="https://imos.org.au/resources/acknowledging-us",
                                    style={
                                        "font-size": "16px",  # Adjust font size as needed
                                        "color": "#0c2024",
                                        "text-decoration": "underline",
                                        "font-weight": "bold",
                                    },
                                ),
                                # Footer links directly below acknowledgment content
                                html.Div(
                                    [
                                        html.A(
                                            "Privacy Policy",
                                            href="#",
                                            className="footer-link",
                                            style={
                                                "font-size": "14px",
                                                "margin-right": "5px",
                                            },
                                        ),
                                        html.Span(
                                            " | ",
                                            className="footer-separator",
                                            style={
                                                "font-size": "14px",
                                                "margin-right": "5px",
                                            },
                                        ),
                                        html.A(
                                            "Terms of Service",
                                            href="#",
                                            className="footer-link",
                                            style={
                                                "font-size": "14px",
                                                "margin-left": "5px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "margin-top": "10px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "flex": "1",
                                "text-align": "center",
                                "padding": "0 20px",
                            },  # Centered content
                        ),
                        # App name on the far right with updated logo
                        html.Div(
                            [
                                html.Img(
                                    src="/assets/message-me-logo.png",
                                    style={"height": "40px", "margin-right": "10px"},
                                ),
                                html.P(
                                    f"© 2024 {app_name}",
                                    style={
                                        "font-size": "16px",  # Adjust font size as needed
                                        "font-weight": "bold",
                                        "color": "white",
                                        "margin-bottom": "0",
                                        "text-align": "right",
                                    },
                                ),
                            ],
                            style={
                                "flex": "0 0 auto",
                                "text-align": "right",
                            },
                        ),
                    ],
                ),
            ],
            className="footer",
            style={
                "background": "linear-gradient(180deg, #27B5C1, #1897A6, #118093, #0B657D)",  # Ocean gradient
                "color": "white",
                "padding": "20px 0",  # Adjust padding as needed
                # "position": "fixed",
                "bottom": "0",
                "width": "100%",
                "z-index": "10",
            },
        ),
    ],
)


# Updated Sign-up form layout
signup_layout = html.Div(
    [
        html.Header(
            [
                html.Div(
                    [
                        html.A(
                            href="/home",
                            children=[
                                html.Img(
                                    src="/assets/Gemini_Generated_Image_67twfk67twfk67tw.jfif",
                                    className="logo",
                                    style={
                                        "height": "120px",
                                        "margin-right": "15px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.H1(
                                            app_name,
                                            style={
                                                "margin-bottom": "0px",
                                                "font-size": "36px",
                                                "font-weight": "700",
                                                "color": "Lightgrey",
                                            },
                                        ),
                                    ],
                                    className="header-text",
                                ),
                            ],
                            style={
                                "display": "flex",
                                "align-items": "center",
                                "text-decoration": "none",
                            },
                        ),
                    ],
                    className="header-content",
                ),
                html.Nav(
                    [
                        html.A("Home", href="#home", className="nav-link"),
                        html.A(
                            "Visualizations",
                            href="/home#visualizations",
                            className="nav-link",
                        ),
                        html.A("About", href="#about", className="nav-link"),
                        html.A("Contact", href="#contact", className="nav-link"),
                    ],
                    className="nav-bar",
                    style={"margin-left": "auto"},  # Align nav items to the right
                ),
                # Sign-Up Button with Bell Icon and Dark Blue Background
                html.Div(
                    [
                        html.A(
                            [
                                html.I(
                                    className="fas fa-bell",
                                    style={"color": "red", "margin-right": "10px"},
                                ),
                                "SIGN UP",
                            ],
                            href="/signup",
                            className="sign-up-btn",
                        )
                    ],
                    style={"text-align": "right", "padding-right": "20px"},
                ),
            ],
            className="header",
            id="signup-header",
        ),
        html.Div(
            className="d-flex justify-content-center align-items-center",
            style={"height": "73vh", "padding": "60px"},
            children=[
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-bell",
                                        style={
                                            "font-size": "48px",
                                            "color": "rgb(255 78 22)",
                                            "margin-bottom": "20px",
                                        },
                                    ),
                                ],
                                className="text-center",
                            ),
                            html.H3(
                                "Don't Miss Out on Hot Alerts!",
                                className="card-title text-center",
                                style={
                                    "font-size": "36px",
                                    "font-weight": "bold",
                                    "color": "rgb(255 78 22)",
                                },
                            ),
                            html.P(
                                "Stay informed about critical ocean temperature changes by signing up for our alerts.",
                                className="card-text text-center",
                                style={
                                    "font-size": "20px",
                                    "color": "rgb(84 100 118)",
                                    "margin-top": "24px",
                                    "margin-bottom": "30px",
                                    "font-style": "italic",
                                    "font-weight": "500",
                                },
                            ),
                            dbc.Form(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Label(
                                                    [
                                                        html.I(
                                                            className="fas fa-envelope",
                                                            style={
                                                                "font-size": "18px",
                                                                "color": "rgb(255 78 22)",
                                                                "margin-right": "10px",
                                                            },
                                                        ),
                                                        "Email Address",
                                                    ],
                                                    html_for="email-input",
                                                    style={
                                                        "font-size": "18px",
                                                        "color": "rgb(22 105 155)",
                                                        "font-weight": "600",
                                                    },
                                                ),
                                                width=12,
                                            )
                                        ]
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Input(
                                                    id="email-input",
                                                    placeholder="Enter your email address",
                                                    type="email",
                                                    style={
                                                        "font-size": "18px",
                                                        "padding": "10px",
                                                        "border-radius": "5px",
                                                        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                                        "margin-bottom": "20px",
                                                    },
                                                ),
                                                width=12,
                                            )
                                        ]
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Button(
                                                    "SIGN UP",
                                                    id="signup-button",
                                                    color="primary",
                                                    className="signup-button",
                                                    style={
                                                        "background-image": "linear-gradient(90deg, #FF5733, #FF8D1A, #FFC300)",  # Gradient from deep orange to yellow
                                                        "font-size": "20px",
                                                        "padding": "10px 20px",
                                                        "border-radius": "5px",
                                                        "font-weight": "600",
                                                        "width": "100%",
                                                        "color": "rgb(53 28 14)",
                                                        "border": "none",
                                                        "transition": "background-image 0.3s ease",
                                                    },
                                                ),
                                                width=13,
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            html.Div(
                                id="signup-message",
                                style={
                                    "margin-top": "20px",
                                    "font-size": "18px",
                                    "color": "#006080",
                                    "text-align": "center",
                                },
                            ),
                            html.Div(id="email-store", style={"display": "none"}),
                        ]
                    ),
                    style={
                        "width": "100%",
                        "max-width": "550px",
                        "box-shadow": "#00a69966 0px 5px 6px",
                        "border-radius": "12px",
                    },
                ),
                # Output to display a console message
                # html.Div(id="console-output"),
            ],
        ),
        html.Footer(
            [
                html.Div(
                    className="d-flex justify-content-between align-items-center",
                    style={
                        "padding": "10px 20px",
                        "height": "100px",
                    },
                    children=[
                        # IMOS logo on the far left
                        html.Div(
                            html.Img(
                                src="/assets/footer-logo.png", style={"height": "75px"}
                            ),
                            style={"flex": "0 0 auto"},
                        ),
                        html.Div(
                            [
                                html.P(
                                    "Data were sourced from Australia’s Integrated Marine Observing System (IMOS) – IMOS is enabled by the National Collaborative Research Infrastructure Strategy (NCRIS).",
                                    style={
                                        "font-size": "17px",  # Adjust font size as needed
                                        "color": "white",
                                        "margin-bottom": "0",
                                        "font-weight": "500",
                                    },
                                ),
                                html.P(
                                    "It is operated by a consortium of institutions as an unincorporated joint venture, with the University of Tasmania as Lead Agent.",
                                    style={
                                        "font-size": "17px",  # Adjust font size as needed
                                        "color": "white",
                                        "margin-bottom": "0",
                                        "font-weight": "500",
                                    },
                                ),
                                html.A(
                                    "Acknowledgements",
                                    href="https://imos.org.au/resources/acknowledging-us",
                                    style={
                                        "font-size": "16px",  # Adjust font size as needed
                                        "color": "#0c2024",
                                        "text-decoration": "underline",
                                        "font-weight": "bold",
                                    },
                                ),
                                # Footer links directly below acknowledgment content
                                html.Div(
                                    [
                                        html.A(
                                            "Privacy Policy",
                                            href="#",
                                            className="footer-link",
                                            style={
                                                "font-size": "14px",
                                                "margin-right": "5px",
                                            },
                                        ),
                                        html.Span(
                                            " | ",
                                            className="footer-separator",
                                            style={
                                                "font-size": "14px",
                                                "margin-right": "5px",
                                            },
                                        ),
                                        html.A(
                                            "Terms of Service",
                                            href="#",
                                            className="footer-link",
                                            style={
                                                "font-size": "14px",
                                                "margin-left": "5px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "margin-top": "10px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "flex": "1",
                                "text-align": "center",
                                "padding": "0 20px",
                            },  # Centered content
                        ),
                        # App name on the far right
                        html.Div(
                            html.P(
                                f"© 2024 {app_name}",
                                style={
                                    "font-size": "16px",  # Adjust font size as needed
                                    "font-weight": "bold",
                                    "color": "white",
                                    "margin-bottom": "0",
                                    "text-align": "right",
                                },
                            ),
                            style={
                                "flex": "0 0 auto",
                                "text-align": "right",
                            },
                        ),
                    ],
                ),
            ],
            className="footer",
            style={
                "background": "linear-gradient(180deg, #27B5C1, #1897A6, #118093, #0B657D)",  # Ocean gradient
                "color": "white",
                "padding": "20px 0",  # Adjust padding as needed
                # "position": "fixed",
                "bottom": "0",
                "width": "100%",
                "z-index": "10",
            },
        ),
    ]
)
# Set initial layout to intro page
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


# Callback to switch layouts after intro page
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/signup":
        return signup_layout
    elif pathname == "/":
        return intro_layout
    else:
        return main_layout


@cache.memoize()  # Cache this function's result
def get_plot_data(file_path):
    return load_and_fix_json(file_path)


@app.callback(Output("heatmap-graph", "figure"), Input("url", "pathname"))
def update_heatmap(pathname):
    if pathname != "/":
        return get_plot_data("Figures/MAI090_PercentilesHeatMap.json")
    return {}


@app.callback(Output("temp-dist-plot-graph", "figure"), Input("url", "pathname"))
def update_temp_dist_plot(pathname):
    if pathname != "/":
        return get_plot_data("Figures/Temp_Distribution_MAI_2m.json")
    return {}


@app.callback(Output("temp-dist-plot-graph-21m", "figure"), Input("url", "pathname"))
def update_temp_dist_plot_21m(pathname):
    if pathname != "/":
        return get_plot_data("Figures/Temp_Distribution_MAI_21m.json")
    return {}


@app.callback(Output("daily-spike-graph", "figure"), Input("url", "pathname"))
def update_daily_spike_plot(pathname):
    if pathname != "/":
        return get_plot_data("Figures/plot_all_daily_spike_Summer21-22.json")
    return {}


@app.callback(Output("acumulada-plot-graph", "figure"), Input("url", "pathname"))
def update_acumulada_plot(pathname):
    if pathname != "/":
        return get_plot_data("Figures/Acumulada_2024_plot.json")
    return {}


@app.callback(Output("temp-anom-heatmap-graph", "figure"), Input("url", "pathname"))
def update_temp_anom_heatmap(pathname):
    if pathname != "/":
        return get_plot_data("Figures/MAI090_MHW_per_time_heatmap_TEMP-ANOM.json")
    return {}


@app.callback(
    Output("new-plot-graph", "figure"),
    Input("year-dropdown", "value"),
    Input("depth-dropdown", "value"),
)
def update_new_plot(selected_year, selected_depth):
    return get_plot_data("Figures/micheal-new-plot.json")


@app.callback(Output("rainfall-heatmap-graph", "figure"), Input("url", "pathname"))
def update_rainfall_heatmap(pathname):
    if pathname != "/":
        return get_plot_data("Figures/rainfall_heatmap2004-2024.json")
    return {}


@app.callback(Output("mhw-heatmap-graph", "figure"), Input("url", "pathname"))
def update_mhw_heatmap(pathname):
    if pathname != "/":
        return get_plot_data("Figures/MAI090_MHW_per_time_heatmap-new.json")
    return {}


@app.callback(Output("acumulada-aug-plot-graph", "figure"), Input("url", "pathname"))
def update_acumulada_aug_plot(pathname):
    if pathname != "/":
        return get_plot_data("Figures/Acumulada_Aug-2024_plot.json")
    return {}


# Callback to Trigger hacky script


@app.callback(
    Output("console-output", "children"),  # Output for console messages
    Input("signup-button", "n_clicks"),  # Trigger on button click
    State("email-input", "value"),  # Capture email input value
)

# Trigger the script from SignUp Button
def handle_signup(n_clicks, email_value):
    if n_clicks and email_value:
        stored_email = email_value

        # Print the stored email to the console
        print(f"Stored Email: {stored_email}")

        # Run the external Python script
        try:
            result = subprocess.run(
                ["python", script_path], capture_output=True, text=True
            )
            print(f"Script Output: {result.stdout}")
            return f"Script executed successfully for email: {stored_email}"
        except Exception as e:
            print(f"Error running script: {e}")
            return f"Failed to execute script for email: {stored_email}"

    return "Sign-up button not clicked or email not provided."


# Internal custom CSS and JavaScript for wave effects and animations
app.index_string = (
    """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>"""
    + app_name
    + """</title>
        <link rel="icon" href="/assets/favicon.jfif" type="image/x-icon">
        {%css%}
        <style>
            body {
                background-color: #f8f9fa;
                color: #333333;
                font-family: Arial, sans-serif;
            }
            .animated-search:hover {
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            }

            .animated-search:focus-within {
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            }


            .intro-logo {
                height: 150px;
                margin-bottom: 20px;
            }

            .header {
                background: linear-gradient(180deg, #27B5C1, #1897A6, #118093, #0B657D);
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
                background-image: url('/assets/image.png');
                background-size: cover;
                position: absolute;
                bottom: -50px;
                left: 0;
                right: 0;
                z-index: 5;
            }

            .header-content {
                display: flex;
                align-items: center;
                font-style: none;
            }

            .logo {
                margin-right: 20px;
                height: 150px;
                border-radius: 15px;
                # box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
            }

            .header-text h1, .header-text h4 {
                margin: 0;
            }

           .nav-bar {
    display: flex;
    justify-content: flex-end;
    gap: 20px;
    flex: 1;
    margin-right: 20px;
}

           .nav-link {
    font-size: 22px;
    font-weight: bold;
    padding: 30px 20px;
    color: Lightgrey;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s, color 0.3s;
}

          .nav-link:hover, .nav-link:focus {
    background-color: rgba(39, 181, 193, 0.2);  /* Light blue background on hover */
    color: darkblue;
}
            .search-bar:hover,
            .search-bar:focus-within {
                box-shadow: 0 0 30px 10px rgba(39, 181, 193, 0.7), 0 0 30px 10px rgba(0, 128, 128, 0.7);  /* Gradient-like shadow effect */
                border-color: #0c2024;  
                background-color: ##0c2024;
            }
           
            @keyframes typing {
                from { width: 0 }
                to { width: 100% }
            }

            @keyframes blink-caret {
                from, to { border-color: transparent }
                50% { border-color: orange; }
            }

            .typed-text {
                font-family: Arial, sans-serif;
                font-size: 22px;
                font-weight: 600;
                font-style: italic;
                overflow: hidden; /* Ensures the text is clipped at the boundary */
                white-space: nowrap; /* Keeps the text on a single line */
                border-right: 3px solid orange; /* The caret */
                animation: typing 2s steps(12) 1s 1 normal both, blink-caret 0.75s step-end infinite; /* Typing and caret animations */
                width: 0;  /* Start with zero width */
            }


            .intro-section {
                height: 100vh;
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                position: relative;
                z-index: 1;
                overflow: hidden;
            }

            .intro-text {
                max-width: 50%;
                z-index: 2;
            }

            .content {
                padding: 20px;
            }

            .plot-section {
                margin-bottom: 60px;
                background-color: #EEEEEE;
                color: #333333;
                padding: 20px;
                border-radius: 10px;
            }

            .contact-container {
                margin-bottom: 40px;
                background-color: #002040;
                color: white;
                padding: 20px;
                border-radius: 10px;
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
                background-image: url('/assets/image.png');
                background-size: cover;
                position: absolute;
                top: -50px;
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
                position: relative.
            }

            .footer-link {
                color: white;
                text-decoration: none;
                margin-right: 10px;
            }

            .footer-link:hover {
                text-decoration: underline.
            }

            .footer-separator {
                margin-right: 10px.
                color: #ffffff.
            }

            .intro-section::before {
                content: ''.
                position: absolute.
                top: 0.
                left: 0.
                right: 0.
                bottom: 0.
                background-image: url('/assets/into-section-cover.jfif').
                background-repeat: no-repeat.
                opacity: 0.7.
                z-index: 1.
                animation: oceanWaves 10s infinite linear.
            }

            .intro-section {
                background: linear-gradient(120deg, #002040 0%, #006080 50%, #004080 100%).
                color: white.
            }
            .card-body{
                padding: 68px;
            }

            .sign-up-btn {
    background-color: #172427;
    color: white;
    padding: 20px 20px;
    border-radius: 5px;
    font-size: 21px;
    font-weight: 600;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    transition: background-color 0.3s;
}

.logo {
    height: 60px;
    margin-right: 20px;
}

          .signup-button:hover {
    background-image: #00448a;
    color: white;
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
"""
)
if __name__ == "__main__":
    app.run_server(debug=True)
