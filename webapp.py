import streamlit as st
import plotly.express as px
import pandas as pd

# Set the page configuration
st.set_page_config(
    page_title="Ocean Heatwaves Visualization",
    page_icon="🌊",
    layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
     body {
        background-color: #ffffff;
        color: #333333;
    }

    /* Header styling */
    .header {
        font-size: 36px;
        font-weight: bold;
        color: #ffffff;
        background-color: #007bff;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* App title styling */
    .app-title {
        position: absolute;
        top: 20px;
        left: 20px;
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
    }
    </style>
    <div class="header">
        Ocean Heatwaves Visualization
    </div>
    <div class="app-title">
        🌊 MHW Visualizer
    </div>
    """,
    unsafe_allow_html=True
)

# Example Plotly Visualizations
st.subheader("Example Visualizations")

# Line chart - Example 1
df = pd.DataFrame({
    "Time": pd.date_range("2021-01-01", periods=100),
    "Temperature": pd.Series(range(100)) + pd.Series(range(100)).apply(lambda x: x ** 0.5)
})
fig_line = px.line(df, x="Time", y="Temperature", title="Temperature Over Time", color_discrete_sequence=["#FF5733"])
st.plotly_chart(fig_line, use_container_width=True)

# Scatter chart - Example 2
fig_scatter = px.scatter(
    df,
    x="Time",
    y="Temperature",
    title="Scatter Plot of Temperature",
    color="Temperature",
    color_continuous_scale=px.colors.sequential.Viridis,
    size="Temperature"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Bar chart Example 3
fig_bar = px.bar(df, x="Time", y="Temperature", title="Temperature Bar Chart", color="Temperature", color_continuous_scale=px.colors.sequential.Bluered)
st.plotly_chart(fig_bar, use_container_width=True)
