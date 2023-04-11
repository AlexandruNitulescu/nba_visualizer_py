import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import sqlite3
from sqlite3 import Error
import modules.helper_functions as hlp
from streamlit_extras.metric_cards import style_metric_cards
from PIL import Image

image = Image.open('./img/logo.png')

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
#st.title(':basketball: NBA Visualizer')
st.image(image)
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
t_ppg, t_ast, t_reb, t_stl, t_tov, t_blk, t_pf = calc.calculate_team_stats()
df_count, df_dates, df_min, df_pts, df_fgm =calc.calculate_total_stats()

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgba(28, 131, 225, 0.1);
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: black;
   font-size: large;
}

</style>
"""
, unsafe_allow_html=True)

avg_ppg = t_ppg['ppg'].mean()
avg_astpg = t_ast['astpg'].mean()
avg_rebpg = t_reb['rebpg'].mean()
avg_stlpg = t_stl['stlpg'].mean()
avg_tovpg = t_tov['tovpg'].mean()
avg_blkpg = t_blk['blkpg'].mean()
avg_pfpg = t_pf['pfpg'].mean()

st.header("Summary")
st.markdown("##### NBA Visualizer is a dynamic web app that provides a comprehensive look at the performance of NBA teams during the 2022-23 season. With scraped data and processed in the backend, the app provides insightful visualizations and analysis of key statistics. The user-friendly interface of the app, allows users to interact with the data and explore different visualizations that give them a better understanding of the performance of their favorite teams. With intuitive controls, users can filter and sort the data to focus on specific teams or statistics that interest them the most. NBA Visualizer offers a variety of charts and graphs that allow users to see trends and patterns in the data. From stacked bar charts to scatterplots, users can choose the visualizations that best suit their needs and preferences.")
st.markdown('##### Made by **[Alexandru Nitulescu](https://www.linkedin.com/in/alexandru-nitulescu-035778153/)**')
st.markdown("""---""")


st.header('Total stats of NBA')
col4, col5, col6, col7, col8 = st.columns(5)
with col4:
    st.markdown(f"#### 🏀 {df_count['tot_matches'][0]} Matches Played")
with col5:
    st.markdown(f"#### 📆 {df_dates['tot_dates'][0]} Unique Dates")
with col6:
    tot_date = df_min['tot_minutes'][0]
    formatted_date = '{:,}'.format(tot_date).replace(',', ' ')
    st.markdown(f"#### ⏱️ {formatted_date} Minutes")
with col7:
    tot_pts = df_pts['tot_pts'][0]
    formatted_pts = '{:,}'.format(tot_pts).replace(',', ' ')
    st.markdown(f"#### 🗑️ {formatted_pts} Points")
with col8:
    tot_fgm = df_fgm['tot_fgm'][0]
    formatted_pts = '{:,}'.format(tot_fgm).replace(',', ' ')
    st.markdown(f"#### ⛹️ {formatted_pts} Field Goals")
st.markdown("""---""")

st.header("NBA Team Average Stats")
metric_1, metric_2, metric_3, metric_4, metric_5, metric_6, metric_7 = st.columns(7)

mean_values = calc.calculate_mean_values()
metric_1.metric(label="Points", value=mean_values['avg_pts'][0])
metric_2.metric(label="Assists", value=mean_values['avg_ast'][0])
metric_3.metric(label="Rebounds", value=mean_values['avg_reb'][0])
metric_4.metric(label="Steals", value=mean_values['avg_stl'][0])
metric_5.metric(label="Blocks", value=mean_values['avg_blk'][0])
metric_6.metric(label="Turnovers", value=mean_values['avg_tov'][0])
metric_7.metric(label="Personal Fouls", value=mean_values['avg_pf'][0])
style_metric_cards()

col4, col5, col6, col7, col8 = st.columns(5)
subtab_avg_pts, subtab_avg_ast, subtab_avg_reb, subtab_avg_stl, subtab_avg_blk, subtab_avg_tov, subtab_avg_pf = st.tabs(['**Points per Game**', '**Assists per Game**', '**Rebounds per Game**', 
                                                                                                                        '**Steals per Game**', '**Blocks per Game**', '**Turnovers per Game**', '**Personal Fouls per Game**'])
with subtab_avg_pts:
    c1, c2 = st.columns([2,1])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=t_ppg['team_name'], 
        x=t_ppg['ppg'],
        orientation='h', marker=dict(color=t_ppg['ppg'].apply(lambda x: '#0bb4ff' if x >= avg_ppg else '#e60049'))))
    
    fig.update_layout(
        title={
            'text':'Average Points per Game',
            'font':{
                    'family': 'sans-serif',
                    'size': 14,
                    },
                },
        xaxis_title='Points',
        yaxis_title='',
        xaxis_tickformat='.1f',
        yaxis_autorange='reversed',
        xaxis_showgrid=True,
        xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
        xaxis_ticks='outside',
        yaxis_showgrid=False,
        height=600, width=800,
        font=dict(
            family='sans-serif',
            size=14))
    
    fig.update_xaxes(
        range = [min(t_ppg['ppg']-1), max(t_ppg['ppg']+1)]
    )
    
    c1.plotly_chart(fig, use_container_width=False)
    t_ppg.index = np.arange(1, len(t_ppg) + 1)
    c2.markdown("##### Preview Table of Points per Game")
    c2.dataframe(t_ppg, height=560, use_container_width=True)
with subtab_avg_ast:
    c1, c2 = st.columns([2,1])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=t_ast['team_name'], 
        x=t_ast['astpg'],
        orientation='h', marker=dict(color=t_ast['astpg'].apply(lambda x: '#0bb4ff' if x >= avg_astpg else '#e60049'))))
    
    fig.update_layout(
        title={
            'text':'Average Assists per Game',
            'font':{
                    'family': 'sans-serif',
                    'size': 14,
                    },
                },
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
        range = [min(t_ast['astpg']-1), max(t_ast['astpg']+1)]
    )
    c1.plotly_chart(fig, use_container_width=True)
    t_ast.index = np.arange(1, len(t_ast) + 1)
    c2.markdown("##### Preview Table of Assists per Game")
    c2.dataframe(t_ast, height=560, use_container_width=True)
with subtab_avg_reb:
    c1, c2 = st.columns([2,1])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=t_reb['team_name'], 
        x=t_reb['rebpg'],
        orientation='h', 
        marker=dict(color=t_reb['rebpg'].apply(lambda x: '#0bb4ff' if x >= avg_rebpg else '#e60049'))))
    
    fig.update_layout(
        title={
            'text':'Average Rebounds per Game',
            'font':{
                    'family': 'sans-serif',
                    'size': 14,
                    },
                },
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
        range = [min(t_reb['rebpg']-1), max(t_reb['rebpg']+1)]
    )
    c1.plotly_chart(fig, use_container_width=True)
    t_reb.index = np.arange(1, len(t_reb) + 1)
    c2.markdown("##### Preview Table of Rebounds per Game")
    c2.dataframe(t_reb, height=560, use_container_width=True)
with subtab_avg_stl:
    c1, c2 = st.columns([2,1])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=t_stl['team_name'], 
        x=t_stl['stlpg'],
        orientation='h', 
        marker=dict(color=t_stl['stlpg'].apply(lambda x: '#0bb4ff' if x >= avg_stlpg else '#e60049'))))
    
    fig.update_layout(
        title={
            'text':'Average Steals per Game',
            'font':{
                    'family': 'sans-serif',
                    'size': 14,
                    },
                },
        xaxis_title='Steals',
        xaxis_tickformat='.1f',
        yaxis_autorange='reversed',
        xaxis_showgrid=True,
        xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
        xaxis_ticks='outside',
        yaxis_showgrid=False,
        height=600, width=800,
        font=dict(size=10))
    
    fig.update_xaxes(
        range = [min(t_stl['stlpg']-1), max(t_stl['stlpg']+1)]
    )
    c1.plotly_chart(fig, use_container_width=True)
    t_stl.index = np.arange(1, len(t_stl) + 1)
    c2.markdown("##### Preview Table of Steals per Game")
    c2.dataframe(t_stl, height=560, use_container_width=True)
with subtab_avg_tov:
    c1, c2 = st.columns([2,1])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=t_tov['team_name'], 
        x=t_tov['tovpg'],
        orientation='h', 
        marker=dict(color=t_tov['tovpg'].apply(lambda x: '#0bb4ff' if x >= avg_tovpg else '#e60049'))))
    
    fig.update_layout(
        title={
            'text':'Average Turnovers per Game',
            'font':{
                    'family': 'sans-serif',
                    'size': 14,
                    },
                },
        xaxis_title='Turnovers',
        xaxis_tickformat='.1f',
        yaxis_autorange='reversed',
        xaxis_showgrid=True,
        xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
        xaxis_ticks='outside',
        yaxis_showgrid=False,
        height=600, width=800,
        font=dict(size=10))
    
    fig.update_xaxes(
        range = [min(t_tov['tovpg']-1), max(t_tov['tovpg']+1)]
    )
    c1.plotly_chart(fig, use_container_width=True)
    t_tov.index = np.arange(1, len(t_reb) + 1)
    c2.markdown("##### Preview Table of Turnovers per Game")
    c2.dataframe(t_tov, height=560, use_container_width=True)
with subtab_avg_blk:
    c1, c2 = st.columns([2,1])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=t_reb['team_name'], 
        x=t_blk['blkpg'],
        orientation='h', 
        marker=dict(color=t_blk['blkpg'].apply(lambda x: '#0bb4ff' if x >= avg_blkpg else '#e60049'))))
    
    fig.update_layout(
        title={
            'text':'Average Blocks per Game',
            'font':{
                    'family': 'sans-serif',
                    'size': 14,
                    },
                },
        xaxis_title='Blocks',
        xaxis_tickformat='.1f',
        yaxis_autorange='reversed',
        xaxis_showgrid=True,
        xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
        xaxis_ticks='outside',
        yaxis_showgrid=False,
        height=600, width=800,
        font=dict(size=10))
    
    fig.update_xaxes(
        range = [min(t_blk['blkpg']-1), max(t_blk['blkpg']+1)]
    )
    c1.plotly_chart(fig, use_container_width=True)
    t_blk.index = np.arange(1, len(t_reb) + 1)
    c2.markdown("##### Preview Table of Blocks per Game")
    c2.dataframe(t_blk, height=560, use_container_width=True)
with subtab_avg_pf:
    c1, c2 = st.columns([2,1])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=t_reb['team_name'], 
        x=t_pf['pfpg'],
        orientation='h', 
        marker=dict(color=t_pf['pfpg'].apply(lambda x: '#0bb4ff' if x >= avg_pfpg else '#e60049'))))
    
    fig.update_layout(
        title={
            'text':'Average Personal Fouls per Game',
            'font':{
                    'family': 'sans-serif',
                    'size': 14,
                    },
                },
        xaxis_title='Personal Fouls',
        xaxis_tickformat='.1f',
        yaxis_autorange='reversed',
        xaxis_showgrid=True,
        xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
        xaxis_ticks='outside',
        yaxis_showgrid=False,
        height=600, width=800,
        font=dict(size=10))
    
    fig.update_xaxes(
        range = [min(t_pf['pfpg']-1), max(t_pf['pfpg']+1)]
    )
    c1.plotly_chart(fig, use_container_width=True)
    t_pf.index = np.arange(1, len(t_pf) + 1)
    c2.markdown("##### Preview Table of Personal Fouls per Game")
    c2.dataframe(t_pf, height=560, use_container_width=True)

st.markdown("""---""")
st.header("Match Results")
col9, col10 = st.columns([1, 3])
col9.markdown("Preview Table of Match Results")
df = pd.read_sql('''
            SELECT team_name, 
                    SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) AS wins,
                    SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) AS losses
           FROM team_info 
           JOIN match_info ON team_info.team_id = match_info.team_id
           GROUP BY team_name
           ORDER BY wins DESC''', conn)
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
fig.update_layout(barmode='stack', xaxis_tickangle=-45, height=600)
col10.plotly_chart(fig, use_container_width=True)
col9.dataframe(df, height=560, use_container_width=True)
st.markdown("""---""")

st.header("Correlation between Field Goals Attempted and Field Goal Percentage")
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

fig.update_layout(
                  xaxis_title='Field Goals Attempted',
                  yaxis_title='Field Goal Percentage',
                  height=600)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""---""")

calc = hlp.Calculation(conn)
viz = hlp.Visualisation(conn)

st.header("Match Analyzer")
teams = pd.read_sql(
    '''
    SELECT team_name, team_id
    FROM team_info
    ''', conn
)

teams_dict = teams.set_index('team_id')['team_name'].to_dict()


column1, column2, column3= st.columns([1,1,2])

with column1:
    selected_5 = st.selectbox("Select Team", list(teams_dict.values()))
with column2:
    selected_6 = st.selectbox("Select Teams", list(teams_dict.values()))

selected_team1_id = list(teams_dict.keys())[list(teams_dict.values()).index(selected_5)]
selected_team2_id = list(teams_dict.keys())[list(teams_dict.values()).index(selected_6)]
df, match_ids = calc.get_match_stats(selected_team1_id, selected_team2_id)
with column3:
    options = st.multiselect("MatchIDS", options=match_ids, default=match_ids)
if selected_5 != selected_6:
    st.dataframe(df, use_container_width=True)

column4, column5,column6 = st.columns([1,1,2])
away_col, a_bar, h_bar, home_col = st.columns([1,2,2,1])
header = [x for x in df.columns]

if len(options) == 1:
    match_id_rows = df.loc[df['match_id'] == options[0]]
    row1 = match_id_rows.iloc[0].tolist()
    row2 = match_id_rows.iloc[1].tolist()
    selected = True
    if row1[1] in row1[0]:
        home_stats = row1
        away_stats = row2
    else:
        home_stats = row2
        away_stats = row1
elif len(options)>1:
    st.warning('Multiple id(s) will not show you match analysis. Filter down to a singular match.', icon="⚠️")

else:
    st.warning('No match id(s) have been selected. Select a specific game in order to take part of match analysis.', icon="⚠️")

################
################

st.header('Match Analyzer')
st.markdown("""---""")

if len(options) == 1:
    match_id_rows = df.loc[df['match_id'] == options[0]]
    row1 = match_id_rows.iloc[0].tolist()
    row2 = match_id_rows.iloc[1].tolist()

    if row1[1] in row1[0]:
        home_stats = row1
        away_stats = row2
    else:
        home_stats = row2
        away_stats = row1
    # game_date = pd.read_sql_query(f'''
    #     SELECT game_date 
    #     FROM game_dates
    #     wHERE date_id ={row1[2]}''', conn).iloc[0].item()
    # st.markdown(f"Home stats: {home_stats}")
    # st.markdown(f"Away stats:{away_stats}")

    l_space, c1, c2, c3, c4, r_space  = st.columns((0.2, .8, 3, 3, .8, 0.2))
    with l_space:
        st.empty()
    with c1:
        pass

    with c2:
        st.markdown(f"<h2 style='text-align: right;'>{away_stats[2]}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{away_stats[-1]}</h2>", unsafe_allow_html=True)
        fig = viz.create_bar(away_stats[3], away_stats[4], home=False, title="FGM", title2="Miss")
        st.plotly_chart(fig, use_container_width=True)
        fig = viz.create_bar(away_stats[5], away_stats[6], home=False, title="TPM", title2="Miss")
        st.plotly_chart(fig, use_container_width=True)
        fig = viz.create_bar(away_stats[7], away_stats[8], home=False, title="FTM", title2="Miss")
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        st.markdown(f"<h2 style='text-align: left;'>{home_stats[2]}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{home_stats[-1]}</h2>", unsafe_allow_html=True)
        fig1 = viz.create_bar(home_stats[3], home_stats[4], home=True, title="FGM", title2="Miss")
        st.plotly_chart(fig1, use_container_width=True)
        fig1 = viz.create_bar(home_stats[5], home_stats[6], home=True, title="TPM", title2="Miss")
        st.plotly_chart(fig1, use_container_width=True)
        fig1 = viz.create_bar(home_stats[7], home_stats[8], home=True, title="FTM", title2="Miss")
        st.plotly_chart(fig1, use_container_width=True)
        fig1 = viz.create_bar(home_stats[10], home_stats[9], home=True, title="DREB", title2="OREB")
        st.plotly_chart(fig1, use_container_width=True)
        fig1 = viz.create_bar(home_stats[9], home_stats[10], home=True, title="OREB", title2="")
        st.plotly_chart(fig1, use_container_width=True)
    with c4:
        pass
    with r_space:
        st.empty()