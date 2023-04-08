import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import sqlite3
from sqlite3 import Error
import modules.helper_functions as hlp
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(
    page_title="NBA Visualizer by Alexandru Nitulescu",
    page_icon=":basketball:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def sidebar():
    st.sidebar.header('Documentation')
    st.sidebar.info("For more information, please see the documentation at the following link: [Documentation](https://example.com/documentation)")

sidebar()

st.title('NBA Visualizer')

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
viz = hlp.Visualisation(conn)
calc = hlp.Calculation(conn)

col1, col2 = st.columns(2)
metric_1, metric_2, metric_3, metric_4, metric_5, metric_6, metric_7 = st.columns(7)

team_ppg = pd.read_sql('''
    SELECT t.team_name, round(AVG(mi.pts), 2) as ppg
    FROM team_info t
    JOIN match_info mi ON t.team_id = mi.team_id
    GROUP BY t.team_name
    ORDER BY ppg DESC
''', conn)
avg_ppg = team_ppg['ppg'].mean()

team_astpg = pd.read_sql('''
    SELECT t.team_name, round(AVG(mi.ast), 2) as astpg
    FROM team_info t
    JOIN match_stats mi ON t.team_id = mi.team_id
    GROUP BY t.team_name
    ORDER BY astpg DESC
''', conn)
avg_astpg = team_astpg['astpg'].mean()

team_rebpg = pd.read_sql('''
    SELECT t.team_name, round(AVG(mi.reb), 2) as rebpg
    FROM team_info t
    JOIN match_stats mi ON t.team_id = mi.team_id
    GROUP BY t.team_name
    ORDER BY rebpg DESC
''', conn)
avg_rebpg = team_rebpg['rebpg'].mean()


col1.header("NBA Team Average Stats")
col1.markdown("Description: The following metrics show the average performance of NBA teams in terms of points, assists, rebounds, steals, blocks, turnovers, and personal fouls during the current 2022-23 season.")
mean_values = calc.calculate_mean_values()
metric_1.metric(label="Points", value=mean_values['avg_pts'][0])
metric_2.metric(label="Assists", value=mean_values['avg_ast'][0])
metric_3.metric(label="Rebounds", value=mean_values['avg_reb'][0])
metric_4.metric(label="Steals", value=mean_values['avg_stl'][0])
metric_5.metric(label="Blocks", value=mean_values['avg_blk'][0])
metric_6.metric(label="Turnovers", value=mean_values['avg_tov'][0])
metric_7.metric(label="Personal Fouls", value=mean_values['avg_pf'][0])
style_metric_cards()


subtab_avg_pts, subtab_avg_ast, subtab_avg_reb = st.tabs(['**AVG PPG**', '**AVG AST**', '**AVG REB**'])
with subtab_avg_pts:
    c1, c2 = st.columns([2,1])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=team_ppg['team_name'], 
        x=team_ppg['ppg'],
        orientation='h', marker=dict(color=team_ppg['ppg'].apply(lambda x: '#0bb4ff' if x >= avg_ppg else '#e60049'))))
    
    fig.update_layout(
        title='Average Points per Game (NBA 2022-23)',
        xaxis_title='Points',
        yaxis_title='',
        xaxis_tickformat='.1f',
        yaxis_autorange='reversed',
        xaxis_showgrid=True,
        xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
        xaxis_ticks='outside',
        yaxis_showgrid=False,
        height=600, width=800,
        font=dict(size=12))
    
    fig.update_xaxes(
        range = [min(team_ppg['ppg']-1), max(team_ppg['ppg']+1)]
    )
    
    c1.plotly_chart(fig, use_container_width=False)
    team_ppg.index = np.arange(1, len(team_ppg) + 1)
    c2.dataframe(team_ppg, height=560, use_container_width=True)

with subtab_avg_ast:
    c1, c2 = st.columns([2,1])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=team_astpg['team_name'], 
        x=team_astpg['astpg'],
        orientation='h', marker=dict(color=team_astpg['astpg'].apply(lambda x: '#0bb4ff' if x >= avg_astpg else '#e60049'))))
    
    fig.update_layout(
        title='Average Assists per Game (NBA 2022-23)',
        xaxis_title='Assists',
        xaxis_tickformat='.1f',
        yaxis_autorange='reversed',
        xaxis_showgrid=True,
        xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
        xaxis_ticks='outside',
        yaxis_showgrid=False,
        height=600, width=800,
        font=dict(size=10))
    
    fig.update_xaxes(
        range = [min(team_astpg['astpg']-1), max(team_astpg['astpg']+1)]
    )
    c1.plotly_chart(fig, use_container_width=True)
    team_astpg.index = np.arange(1, len(team_astpg) + 1)
    c2.dataframe(team_astpg, height=560, use_container_width=True)
with subtab_avg_reb:
    c1, c2 = st.columns([2,1])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=team_rebpg['team_name'], 
        x=team_rebpg['rebpg'],
        orientation='h', 
        marker=dict(color=team_rebpg['rebpg'].apply(lambda x: '#0bb4ff' if x >= avg_rebpg else '#e60049'))))
    
    fig.update_layout(
        title='Average Rebounds per Game (2022-23)',
        xaxis_title='Rebounds',
        xaxis_tickformat='.1f',
        yaxis_autorange='reversed',
        xaxis_showgrid=True,
        xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
        xaxis_ticks='outside',
        yaxis_showgrid=False,
        height=600, width=800,
        font=dict(size=10))
    
    fig.update_xaxes(
        range = [min(team_rebpg['rebpg']-1), max(team_rebpg['rebpg']+1)]
    )
    c1.plotly_chart(fig, use_container_width=True)
    team_rebpg.index = np.arange(1, len(team_astpg) + 1)
    c2.dataframe(team_rebpg, height=560, use_container_width=True)

col3, col4 = st.columns([4,1])
query = '''SELECT team_name, 
                  SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) AS wins,
                  SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) AS losses
           FROM team_info 
           JOIN match_info ON team_info.team_id = match_info.team_id
           GROUP BY team_name
           ORDER BY wins DESC'''
df = pd.read_sql(query, conn)
df.index = np.arange(1, len(df) + 1)
fig = go.Figure()
fig.add_trace(go.Bar
            (x=df['team_name'], 
            y=df['wins'], 
            name='Wins',
            marker=dict(color='#50e991')))

fig.add_trace(go.Bar
            (x=df['team_name'], 
            y=df['losses'], 
            name='Losses',
            marker=dict(color='#e60049')))
fig.update_layout(barmode='stack', title='Wins and Losses',xaxis_tickangle=-45, height=600)
col3.plotly_chart(fig, use_container_width=True)
col4.dataframe(df, height=560, use_container_width=True)

df = pd.read_sql('''
    SELECT fga, fgp
    FROM match_stats
''', conn)

df['fgp_scaled'] = (df['fgp'] - df['fgp'].min()) / (df['fgp'].max() - df['fgp'].min())
df['marker_size'] = df['fga'] * df['fgp_scaled']
color_scale = [[0.0, '#e60049'], [0.5, '#e6d800'], [1.0, '#00bfa0']]
 
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['fga'], y=df['fgp'], mode='markers',
                         marker=dict(size=df['marker_size']/5, color=df['marker_size'], 
                                    colorscale=color_scale, colorbar=dict(title='Marker size'),
                                    line=dict(color='gray', width=1))))

fig.update_layout(title='Correlation between Field Goals Attempted and Field Goal Percentage',
                  xaxis_title='Field Goals Attempted',
                  yaxis_title='Field Goal Percentage',height=600)

st.plotly_chart(fig, use_container_width=True)

# Load data from SQL database
df = pd.read_sql('''
    SELECT fga
    FROM match_stats
''', conn)

# Create a histogram using Plotly
fig = go.Figure()
fig.add_trace(go.Histogram(x=df['fga'], nbinsx=50))

# Add axis labels and title
fig.update_layout(title='Histogram of Field Goals Attempted',
                  xaxis_title='Field Goals Attempted',
                  yaxis_title='Frequency')

# Show the chart
st.plotly_chart(fig)
st.write(f'{len(df)}')

# Load data from SQL database
query = """
SELECT team_name, AVG(fgm) AS fgm, AVG(ast) AS ast, AVG(reb) AS reb
FROM match_stats
JOIN team_info ON team_info.team_id = match_stats.team_id
GROUP BY team_name
"""
df = pd.read_sql(query, conn)

# Create Ternary Scatter Plot using Plotly
fig = px.scatter_ternary(df, a="fgm", b="ast", c="reb", color="team_name", 
                         size_max=10, hover_name="team_name", 
                         title='Ternary Scatter Plot of Teams Based on FGM, AST, and REB')
fig.update_layout(ternary={"sum":1, "aaxis":{"title":"FGM"}, "baxis":{"title":"AST"}, "caxis":{"title":"REB"}})
st.plotly_chart(fig, use_container_width=True)

# Load data from SQL database
df = pd.read_sql('''
    SELECT team_name, AVG(fgm) AS avg_fgm, AVG(ast) AS avg_ast, AVG(reb) AS avg_reb
    FROM match_stats ms
    JOIN team_info ON ms.team_id = team_info.team_id
    GROUP BY team_name
''', conn)

# Create a ternary scatter plot using Plotly
fig = go.Figure(go.Scatterternary(
    a=df['avg_fgm'], b=df['avg_ast'], c=df['avg_reb'],
    mode='markers',
    marker=dict(
        symbol='circle',
        sizemode='diameter',
        sizeref=0.85,
        size=10,
        color='blue',
        opacity=0.7,
    ),
    text=df['team_name'],
    hoverinfo='text',
))

# Add axis labels and title
fig.update_layout(title='Ternary Scatter Plot of Teams Based on FGM, AST, and REB',
                  ternary=dict(sum=100, 
                               aaxis=dict(title='FGM'), 
                               baxis=dict(title='AST'), 
                               caxis=dict(title='REB')))

# Show the chart
st.plotly_chart(fig,use_container_width=True)