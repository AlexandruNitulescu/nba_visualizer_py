import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from sqlite3 import Error

st.set_page_config(
    page_title="TEST by Alexandru Nitulescu",
    page_icon=":file_cabinet:",
    layout="wide",
    initial_sidebar_state="expanded",
)

color_palette = ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"]

st.title('TEST PAGE')

@st.cache_resource
def create_connection(db_file: str) -> sqlite3.Connection:
    '''
    Create a connection to an SQLite database file.
    Args:
        db_file (str): Path to the database file.
    Returns:
        conn (sqlite3.Connection): A Connection object representing the database connection.
    '''
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        print(f"Connection with {db_file} is sucessful!")
        return conn
    except Error as e:
        print(e)
    return conn

conn = create_connection('nba.db')

query = '''SELECT team_name, COUNT(result) AS wins
           FROM team_info JOIN match_info ON team_info.team_id = match_info.team_id
           WHERE result = 'W'
           GROUP BY team_name'''
df = pd.read_sql(query, conn)
# Calculate the mean value of the wins column
mean_wins = df['wins'].mean()

# Create a list of colors for the bars based on their value relative to the mean
colors = ['#50e991' if x > mean_wins else '#ff0000' for x in df['wins']]

# Create the bar chart using Plotly
fig = px.bar(df, x='team_name', y='wins', title='Total Number of Wins per Team', color=colors)

# Add a horizontal line at the mean value
fig.add_shape(type='line', x0=-0.5, x1=len(df)-0.5, y0=mean_wins, y1=mean_wins, line=dict(color='#000000', width=2))

# Show the chart
st.plotly_chart(fig)
# Create the bar chart using Plotly
#fig = px.bar(df, x='team_name', y='wins', title='Total Number of Wins per Team')

# Show the chart
#st.plotly_chart(fig)

query = '''SELECT team_name, COUNT(result) AS wins
           FROM team_info JOIN match_info ON team_info.team_id = match_info.team_id
           WHERE result = 'W'
           GROUP BY team_name'''
df = pd.read_sql(query, conn)

# Create the bar chart using Plotly
fig = px.bar(df, x='team_name', y='wins', title='Total Number of Wins per Team')

# Show the chart
st.plotly_chart(fig)

# Retrieve the data from the database and store it in a pandas dataframe
query = '''SELECT team_name, 
                  SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) AS wins,
                  SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) AS losses
           FROM team_info 
           JOIN match_info ON team_info.team_id = match_info.team_id
           GROUP BY team_name
           ORDER BY wins DESC'''
df = pd.read_sql(query, conn)

# Create the stacked bar chart using Plotly
fig = go.Figure()
fig.add_trace(
    go.Bar(x=df['team_name'], 
           y=df['wins'], 
           name='Wins'))
fig.add_trace(go.Bar(x=df['team_name'], y=df['losses'], name='Losses'))
fig.update_layout(barmode='stack', title='Wins and Losses per Team')
fig.update_xaxes(categoryorder='total descending')

# Show the chart
st.plotly_chart(fig)



# Retrieve the data from the database and store it in a pandas dataframe
query = '''SELECT team_name, 
                  SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) AS wins,
                  SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) AS losses
           FROM team_info 
           JOIN match_info ON team_info.team_id = match_info.team_id
           GROUP BY team_name
           ORDER BY wins DESC'''
df = pd.read_sql(query, conn)

# Create the stacked bar chart using Plotly
fig = go.Figure()
fig.add_trace(go.Bar(x=df['team_name'], y=df['wins'], name='Wins',
                     marker=dict(color=df['wins'].apply(lambda x: '#003f5c' if x >= 40 else '#665191'))))
fig.add_trace(go.Bar(x=df['team_name'], y=df['losses'], name='Losses',
                     marker=dict(color='#f95d6a')))
fig.update_layout(barmode='stack', title='Wins and Losses per Team', xaxis=dict(showgrid=False))

st.plotly_chart(fig)


fig = go.Figure()
fig.add_trace(go.Bar(y=df['team_name'], x=df['wins'], name='Wins',
                     orientation='h', marker=dict(color=df['wins'].apply(lambda x: '#003f5c' if x >= 40 else '#665191'))))
fig.add_trace(go.Bar(y=df['team_name'], x=df['losses'], name='Losses',
                     orientation='h', marker=dict(color='#f95d6a')))
fig.update_layout(barmode='stack', title='Wins and Losses per Team', xaxis=dict(showgrid=False))
st.plotly_chart(fig)