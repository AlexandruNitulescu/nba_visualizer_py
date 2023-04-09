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
        df = pd.read_sql('''
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
        ''', self.conn)
        return df
    
    def calc_ppg(self):
        df = pd.read_sql('''
            SELECT t.team_name, round(AVG(mi.pts), 2) as ppg
            FROM team_info t
            JOIN match_info mi ON t.team_id = mi.team_id
            GROUP BY t.team_name
            ORDER BY ppg DESC
        ''', self.conn)
        return df 
    
    def calculate_team_stats(self):
        df_ppg = pd.read_sql('''
            SELECT t.team_name, round(AVG(mi.pts), 2) as ppg
            FROM team_info t
            JOIN match_info mi ON t.team_id = mi.team_id
            GROUP BY t.team_name
            ORDER BY ppg DESC
        ''', self.conn)

        df_astpg = pd.read_sql('''
            SELECT t.team_name, round(AVG(mi.ast), 2) as astpg
            FROM team_info t
            JOIN match_stats mi ON t.team_id = mi.team_id
            GROUP BY t.team_name
            ORDER BY astpg DESC
        ''', self.conn)

        df_rebpg = pd.read_sql('''
            SELECT t.team_name, round(AVG(mi.reb), 2) as rebpg
            FROM team_info t
            JOIN match_stats mi ON t.team_id = mi.team_id
            GROUP BY t.team_name
            ORDER BY rebpg DESC
        ''', self.conn)

        df_tovpg = pd.read_sql('''
            SELECT t.team_name, round(AVG(mi.tov), 2) as tovpg
            FROM team_info t
            JOIN match_stats mi ON t.team_id = mi.team_id
            GROUP BY t.team_name
            ORDER BY tovpg DESC
        ''', self.conn)

        df_stlpg = pd.read_sql('''
            SELECT t.team_name, round(AVG(mi.stl), 2) as stlpg
            FROM team_info t
            JOIN match_stats mi ON t.team_id = mi.team_id
            GROUP BY t.team_name
            ORDER BY stlpg DESC
        ''', self.conn)

        df_blkpg = pd.read_sql('''
            SELECT t.team_name, round(AVG(mi.blk), 2) as blkpg
            FROM team_info t
            JOIN match_stats mi ON t.team_id = mi.team_id
            GROUP BY t.team_name
            ORDER BY blkpg DESC
        ''', self.conn)

        df_pfpg = pd.read_sql('''
            SELECT t.team_name, round(AVG(mi.pf), 2) as pfpg
            FROM team_info t
            JOIN match_stats mi ON t.team_id = mi.team_id
            GROUP BY t.team_name
            ORDER BY pfpg DESC
        ''', self.conn)
        
        return df_ppg, df_astpg, df_rebpg, df_stlpg, df_tovpg, df_blkpg, df_pfpg
    
    def calculate_total_stats(self):
        df_min = pd.read_sql('''
            SELECT SUM(min) as tot_minutes
            FROM(
                SELECT DISTINCT match_id, min
                FROM match_info)
        ''', self.conn)    
        
        df_count = pd.read_sql('''
            SELECT COUNT(DISTINCT match_id) as tot_matches
            FROM match_info
        ''', self.conn)  
        
        df_dates = pd.read_sql('''
            SELECT COUNT(DISTINCT date_id) as tot_dates
            FROM game_dates
        ''', self.conn)      
        
        df_fgm = pd.read_sql('''
            SELECT SUM(fgm) as tot_fgm
            FROM match_stats
        ''', self.conn)   

        df_points = pd.read_sql('''
            SELECT SUM(pts) as tot_pts
            FROM match_info
        ''', self.conn)  

        return df_count, df_dates, df_min, df_points, df_fgm

