import streamlit as st
import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np

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

st.header("Match Analyzer")
options_1 = ["Maximum", "Minimum"]
options_2 = ["Points", "Assists", "Rebounds", "Steals", "Turnovers", "Blocks"]
options_3 = ["by both Teams combined","by a Team", "difference between Teams"]

# Create the three selectbox widgets
col_1, col_2, col_3 = st.columns(3)
with col_1:
    selected_1 = st.selectbox("Select Maximum or Minimum", options_1)
with col_2:
    selected_2 = st.selectbox("Select a statistic", options_2)
with col_3:
    selected_3 = st.selectbox("Select how to display the statistic", options_3)

stat_value = pd.read_sql('''
                SELECT match_id, SUM(pts) AS total_points
                FROM match_info
                GROUP BY match_id
                ORDER BY total_points
            ''', conn)
if selected_1 == "Maximum":
    stat_value.sort_values(by="total_points", ascending=False, inplace=True)
    stat_value.index = np.arange(1, len(stat_value) + 1)
    st.dataframe(stat_value)

elif selected_1 == "Minimum":
    stat_value.sort_values(by="total_points", ascending=True, inplace=True)
    stat_value.index = np.arange(1, len(stat_value) + 1)
    st.dataframe(stat_value)
