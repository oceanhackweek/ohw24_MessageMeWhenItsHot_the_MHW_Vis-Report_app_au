import dash  # type: ignore
from dash import dcc, html, Input, Output, State  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import plotly.io as pio
import json
import time
from flask_caching import Cache


# Suggested name for the web app
app_name = "Message Me When It's Hot"

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/custom.css"],
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
        "CACHE_TYPE": "simple",  # Using simple cache; for production, you can use Redis or Memcached
        "CACHE_DEFAULT_TIMEOUT": 300,  # Cache timeout in seconds
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


# Function to send email alerts
# def send_email_alert(to_email, subject, body):
#     smtp_server = 'smtp.gmail.com'
#     smtp_port = 587
#     sender_email = 'cartooncoveinfo@gmail.com'  # Replace with your email
#     sender_password = 'ILoveC$iro16'  # Replace with your app password or actual password if 2FA is off

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = to_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, to_email, msg.as_string())
#         server.quit()
#         return True
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         return False

# def send_email_alert(to_email, subject, body):
#     try:
#         yag = yagmail.SMTP('cartooncoveinfo@gmail.com','ILoveC$iro16')  # Replace with your email and app password
#         yag.send(to=to_email, subject=subject, contents=body)
#         return True
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         return False

# Introductory page layout
intro_layout = html.Div(
    style={
        "backgroundColor": "#f8f9fa",
        "height": "100vh",
        "position": "relative",
        "overflow": "hidden",
    },
    children=[
        html.Div(
            [
                html.Img(src="/assets/new-logo-ohw.jfif", className="intro-logo"),
                html.H1(
                    app_name,
                    style={
                        "font-size": "64px",
                        "color": "white",
                        "text-align": "center",
                    },
                ),
                # html.H4("Visualizing the changing temperatures of our oceans", style={'font-size': '24px', 'color': 'white', 'text-align': 'center'}),
            ],
            className="intro-text",
            style={
                "position": "absolute",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "z-index": "2",
                "text-align": "center",
            },
        ),
        html.Div(
            [
                html.Img(
                    src="/assets/Gemini_Generated_Image_eh4irueh4irueh4i.jfif",
                    className="intro-background",
                    style={
                        "width": "100%",
                        "height": "100%",
                        "object-fit": "cover",
                        "position": "absolute",
                        "top": "0",
                        "left": "0",
                        "z-index": "1",
                    },
                )
            ]
        ),
    ],
)

# Video cover section with blur overlay and search bar
video_cover_section = html.Section(
    [
        html.Div(
            [
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
                html.Div(
                    style={
                        "position": "absolute",
                        "top": "0",
                        "left": "0",
                        "right": "0",
                        "bottom": "0",
                        "background-color": "rgba(0, 0, 0, 0.5)",
                        "z-index": "2",
                        "backdrop-filter": "blur(5px)",
                    }
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dbc.Input(
                                    id="location-search",
                                    placeholder="Search Location...",
                                    type="text",
                                    style={
                                        "font-size": "24px",
                                        "padding": "10px",
                                        "border-radius": "25px",
                                        "width": "50%",
                                        "display": "inline-block",
                                    },
                                ),
                                html.I(
                                    className="fas fa-search",
                                    style={
                                        "font-size": "24px",
                                        "color": "white",
                                        "margin-left": "10px",
                                        "vertical-align": "middle",
                                    },
                                ),
                            ],
                            style={"text-align": "center", "margin-top": "25vh"},
                        )
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
        # Header with Wave Design and Logo
        html.Header(
            [
                html.Div(
                    [
                        html.Img(src="/assets/new-logo-ohw.jfif", className="logo"),
                        html.Div(
                            [
                                html.H1(
                                    app_name,
                                    style={"margin-bottom": "0px", "font-size": "32px"},
                                ),
                            ],
                            className="header-text",
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
                        html.A(
                            [html.I(className="fas fa-user-plus"), " Sign Up"],
                            href="/signup",
                            className="nav-link",
                        ),
                    ],
                    className="nav-bar",
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
                                "font-size": "42px",
                                "color": "#333333",
                                "text-align": "center",
                                "font-weight": "bold",
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
        # Visualization Sections with Loading Spinner
        # html.Section([
        #     html.H3([html.I(className="fas fa-chart-line"), " Daily Average Temperature Plot"], style={'font-size': '34px', 'color': '#006080', 'text-align': 'center', 'font-weight': 'bold'}),
        #     html.P([html.I(className="fas fa-info-circle"),
        #             " This plot shows the daily average ocean temperatures, providing insights into temperature trends over time."],
        #            style={'font-size': '20px', 'color': '#004080', 'text-align': 'center', 'margin-bottom': '20px'}),
        #     dcc.Loading(
        #         id="loading-1",
        #         type="default",
        #         children=dcc.Graph(id='daily-avg-plot-graph')
        #     )
        # ], className="plot-section", style={'padding': '20px', 'margin': '60px 0'}),
        html.Main(
            [
                html.Section(
                    [
                        html.H3(
                            [
                                html.I(className="fas fa-thermometer-half"),
                                " Ocean Temperature Percentiles Heat Map",
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
                                html.I(className="fas fa-thermometer-half"),
                                " New's Ocean Temperature Heat Map ",
                                html.Span(
                                    "2012, 2m",
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
                                " This plot shows the ocean temperature heat map for the year 2012 at a depth of 2 meters. You can explore different years and depths to see how the temperature varies.",
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
                                dcc.Dropdown(
                                    id="year-dropdown",
                                    options=[
                                        {"label": str(year), "value": year}
                                        for year in range(2010, 2021)
                                    ],
                                    value=2012,
                                    style={"width": "48%", "display": "inline-block"},
                                ),
                                dcc.Dropdown(
                                    id="depth-dropdown",
                                    options=[
                                        {"label": f"{depth}m", "value": depth}
                                        for depth in [2, 10, 21]
                                    ],
                                    value=2,
                                    style={
                                        "width": "48%",
                                        "display": "inline-block",
                                        "marginLeft": "4%",
                                    },
                                ),
                            ],
                            style={"marginBottom": "20px"},
                        ),
                        dcc.Loading(
                            id="loading-5",
                            type="default",
                            children=dcc.Graph(id="new-plot-graph"),
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
            ],
            className="content",
        ),
        # About Us Section
        html.Section(
            [
                html.Div(
                    [
                        html.H3(
                            "About Us",
                            style={
                                "font-size": "36px",
                                "color": "#333333",
                                "text-align": "center",
                            },
                        ),
                        html.P(
                            "We are dedicated to providing detailed and accurate visualizations of ocean temperature data. Our mission is to help people understand the effects of ocean temperature changes on marine life and global climate.",
                            style={
                                "font-size": "18px",
                                "color": "#666666",
                                "text-align": "center",
                                "padding": "20px",
                            },
                        ),
                    ],
                    style={
                        "padding": "60px 20px",
                        "backgroundColor": "#f0f0f0",
                        "border-radius": "10px",
                    },
                )
            ],
            id="about",
        ),
        # Contact Us Section
        html.Section(
            [
                html.Div(
                    [
                        html.H3(
                            "Contact Us",
                            style={
                                "font-size": "36px",
                                "color": "#333333",
                                "text-align": "center",
                            },
                        ),
                        html.P(
                            "For inquiries, collaborations, or feedback, feel free to reach out to us.",
                            style={
                                "font-size": "18px",
                                "color": "#666666",
                                "text-align": "center",
                            },
                        ),
                        html.P(
                            "Email: info@oceantempvisualizer.com",
                            style={
                                "font-size": "18px",
                                "color": "#666666",
                                "text-align": "center",
                            },
                        ),
                        html.P(
                            "Phone: +1 (123) 456-7890",
                            style={
                                "font-size": "18px",
                                "color": "#666666",
                                "text-align": "center",
                            },
                        ),
                    ],
                    style={
                        "padding": "60px 20px",
                        "backgroundColor": "#f0f0f0",
                        "border-radius": "10px",
                    },
                )
            ],
            id="contact",
        ),
        # Footer with Wave Design
        html.Footer(
            [
                html.Div(
                    [
                        html.P(f"© 2024 {app_name}"),
                        html.P(
                            "Disclaimer: The data and information presented on this dashboard are provided for informational purposes only. "
                            "While every effort has been made to ensure the accuracy of the data, users should verify information before relying on it. "
                            f"{app_name} and its affiliates do not accept any responsibility for any loss or damage caused by use of the information contained herein."
                        ),
                    ],
                    className="footer-content",
                ),
                html.Div(
                    [
                        html.A("Privacy Policy", href="#", className="footer-link"),
                        html.Span(" | ", className="footer-separator"),
                        html.A("Terms of Service", href="#", className="footer-link"),
                    ],
                    className="footer-links",
                ),
            ],
            className="footer",
        ),
        # Collaborators Section
        html.Section(
            [
                html.Div(
                    [
                        html.H3(
                            "Project Collaborators",
                            style={
                                "font-size": "36px",
                                "color": "#333333",
                                "text-align": "center",
                            },
                        ),
                        html.P(
                            "John Doe, Jane Smith, Alex Johnson",
                            style={
                                "font-size": "18px",
                                "color": "#666666",
                                "text-align": "center",
                            },
                        ),
                    ],
                    style={"padding": "20px 0", "text-align": "center"},
                )
            ]
        ),
    ],
)


# Sign-up page layout
signup_layout = html.Div(
    [
        html.Header(
            [
                html.Div(
                    [
                        html.Img(src="/assets/new-logo-ohw.jfif", className="logo"),
                        html.Div(
                            [
                                html.H1(
                                    app_name,
                                    style={"margin-bottom": "0px", "font-size": "32px"},
                                ),
                            ],
                            className="header-text",
                        ),
                    ],
                    className="header-content",
                ),
                html.Nav(
                    [
                        html.A("Home", href="/", className="nav-link"),
                        html.A(
                            "Visualizations",
                            href="#visualizations",
                            className="nav-link",
                        ),
                        html.A("About", href="#about", className="nav-link"),
                        html.A("Contact", href="#contact", className="nav-link"),
                    ],
                    className="nav-bar",
                ),
            ],
            className="header",
            id="signup-header",
        ),
        # Sign-up form
        html.Section(
            [
                html.Div(
                    [
                        html.H3(
                            "Sign Up for Alerts",
                            style={
                                "font-size": "42px",
                                "color": "#333333",
                                "text-align": "center",
                            },
                        ),
                        html.P(
                            "Enter your email address to receive alerts when ocean temperatures reach critical levels.",
                            style={
                                "font-size": "18px",
                                "color": "#666666",
                                "text-align": "center",
                            },
                        ),
                        dbc.Input(
                            id="email-input",
                            placeholder="Enter your email address",
                            type="email",
                            style={
                                "font-size": "18px",
                                "padding": "10px",
                                "margin": "20px 0",
                            },
                        ),
                        dbc.Button(
                            "Sign Up",
                            id="signup-button",
                            color="primary",
                            style={"font-size": "20px", "padding": "10px 20px"},
                        ),
                        html.Div(
                            id="signup-message",
                            style={
                                "margin-top": "20px",
                                "font-size": "18px",
                                "color": "#006080",
                            },
                        ),
                    ],
                    style={"text-align": "center", "padding": "40px"},
                )
            ]
        ),
        html.Footer(
            [
                html.Div(
                    [
                        html.P(f"© 2024 {app_name}"),
                        html.P(
                            "Disclaimer: The data and information presented on this dashboard are provided for informational purposes only. "
                            "While every effort has been made to ensure the accuracy of the data, users should verify information before relying on it. "
                            f"{app_name} and its affiliates do not accept any responsibility for any loss or damage caused by use of the information contained herein."
                        ),
                    ],
                    className="footer-content",
                ),
                html.Div(
                    [
                        html.A("Privacy Policy", href="#", className="footer-link"),
                        html.Span(" | ", className="footer-separator"),
                        html.A("Terms of Service", href="#", className="footer-link"),
                    ],
                    className="footer-links",
                ),
            ],
            className="footer",
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


# Callbacks to load and cache the figures
@cache.memoize()  # Cache this function's result
def get_plot_data(file_path):
    return load_and_fix_json(file_path)


# @app.callback(
#     Output('daily-avg-plot-graph', 'figure'),
#     Input('url', 'pathname')
# )
# def update_daily_avg_plot(pathname):
#     if pathname != "/":
#         return get_plot_data('Figures/DailyAVG_plot.json')
#     return {}


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
        return get_plot_data("Figures/rainfall_heatmap.json")
    return {}


@app.callback(Output("mhw-heatmap-graph", "figure"), Input("url", "pathname"))
def update_mhw_heatmap(pathname):
    if pathname != "/":
        return get_plot_data("Figures/MAI090_MHW_per_time_heatmap.json")
    return {}


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
                z-index: 10;
            }

            .logo {
                margin-right: 20px;
                height: 80px;
                border-radius: 15px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
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
                font-size: 20px;
                font-weight: bold;
            }

            .nav-link:hover {
                text-decoration: underline;
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

            @keyframes oceanWaves {
                0% { background-position: 0% 50%. }
                50% { background-position: 100% 50%. }
                100% { background-position: 0% 50%. }
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
