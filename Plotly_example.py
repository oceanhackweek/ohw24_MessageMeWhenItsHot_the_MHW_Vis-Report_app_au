import matplotlib.pyplot as plt
import plotly.tools as tls
import plotly.io as pio

# Step 1: Create a Matplotlib plot
plt.figure()
plt.plot([1, 2, 3, 4, 5], [10, 11, 12, 13, 14], marker='o')
plt.title('Matplotlib Plot')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')

# Step 2: Convert the Matplotlib figure to a Plotly figure
plotly_fig = tls.mpl_to_plotly(plt.gcf())

# Step 3: Save the Plotly figure as an HTML file
pio.write_html(plotly_fig, file='matplotlib_to_plotly.html', auto_open=True)

# Show the Matplotlib plot
plt.show()
