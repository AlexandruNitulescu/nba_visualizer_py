import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import plotly.subplots as subplots
from streamlit_extras.metric_cards import style_metric_cards
import sqlite3


COLOR_PALETTE = {
    "#003f5c": "Dark Blue",
    "#444e86": "Deep Lavender",
    "#955196": "Plum",
    "#dd5182": "Crimson",
    "#ff6e54": "Vermilion",
    "#ffa600": "Amber"
}

class Visualisation:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.color_palette = COLOR_PALETTE

class Calculation:    
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def calculate_mean_values(self):
        query = '''
           SELECT 
               ROUND(AVG(mi.pts), 2) AS avg_pts,
               ROUND(AVG(ms.ast),2) AS avg_ast,
               ROUND(AVG(ms.reb), 2) AS avg_reb,
               ROUND(AVG(ms.stl), 2) AS avg_stl,
               ROUND(AVG(ms.blk), 2) AS avg_blk,
               ROUND(AVG(ms.tov), 2) AS avg_tov,
               ROUND(AVG(ms.pf), 2) AS avg_pf
           FROM match_stats ms
           JOIN match_info mi ON ms.match_id = mi.match_id
        '''
        df = pd.read_sql(query, self.conn)
        return df