import plotly.express as px
import streamlit as st
import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
import modules.helper_functions as hlp
import plotly.graph_objects as go

# Generate some sample data
x = ['A', 'B', 'C', 'D', 'E']
y = [3, 5, 2, 7, 4]

# Create a bar chart
fig = go.Figure()
fig.add_trace(go.Bar(x=x, y=y))

# Remove the y-axis labels
fig.update_layout(yaxis_title='')

# Show the plot
st.plotly_chart(fig)
