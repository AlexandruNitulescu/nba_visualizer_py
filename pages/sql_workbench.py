import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from sqlite3 import Error

st.set_page_config(
    page_title="SQL Workbench by Alexandru Nitulescu",
    page_icon=":file_cabinet:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('SQL Workbench')

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

col1, col2 = st.columns(2)

def sql_workbench():
    sql_code = col1.text_area('Enter SQL code here', height=100)
    if col1.button('Execute'):
        try:
            my_table = pd.read_sql(f'''{sql_code}''', conn)
            st.write(f"Message: {len(my_table)} row(s) returned")
            st.dataframe(my_table, width=800, height=400, use_container_width=True)

        except Exception as e:
            col1.write("ERROR! SQL command invalid.")

sql_workbench()