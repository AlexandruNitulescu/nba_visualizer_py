import plotly.express as px
import streamlit as st
import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
import modules.helper_functions as hlp
import plotly.graph_objects as go
import  streamlit_toggle as tog

with open("master.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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

st.header('Match Analyzer')
st.divider()

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
    game_date = pd.read_sql_query(f'''
        SELECT game_date 
        FROM game_dates
        wHERE date_id ={row1[2]}''', conn).iloc[0].item()

col41, col51, col61, col71 = st.columns([1,3,3,1])


l_space, c1, c2, c3, c4, r_space  = st.columns((0.2, .8, 3, 3, .8, 0.2))
with l_space:
    st.empty()
with c1:
    st.markdown("<div>👟 Shots on Goal</div>", unsafe_allow_html=True)


with c2:
    st.markdown(f"<h2 style='text-align: right;'>{selected_5}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: right;'>{away_stats[-1]}</h2>", unsafe_allow_html=True)

    st.markdown("<div style='text-align: right;'>👟 Shots on Goal</div>", unsafe_allow_html=True)

with c3:
    st.markdown(f"<h2 style='text-align: left;'>{selected_6}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: left;'>{home_stats[-1]}</h2>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: left;'>👟 Shots on Goal</div>", unsafe_allow_html=True)

with c4:
    st.markdown("<div style='text-align: right;'>👟 Shots on Goal</div>", unsafe_allow_html=True)

with r_space:
    st.empty()