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
    
    def create_match_statsss(self, var, away_team, home_team):
        away_name = away_team[1]
        home_name = home_team[1]
        var = var[2:]
        figs = []
        for i in range(len(var)):
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=away_team[i],
                y=away_name,
                text='test',
                textposition='inside',
                name='',
                orientation='h'))

            fig.add_trace(go.Bar(
                x=home_team[i],
                y=home_name,
                text='test',
                textposition='inside',
                name='',
                orientation='h'
            ))

            fig.update_layout(
                xaxis_title='',
                yaxis_title='',
                barmode='stack',
                showlegend=True,
                legend=dict(x=0.1, y=1.2),
                width=800,
                height=150,
                margin=dict(l=0, r=0, t=80, b=0),
                xaxis=dict(showticklabels=False),
            )
            figs.append(fig)
            return figs
        
        
    def create_match_stats(my_df: pd.DataFrame, away_team, home_team):
        header = [x for x in my_df.iloc[:, 2:]]
        away_name = away_team[1]
        home_name = home_team[1]
        away_team = away_team[2:]
        home_team = home_team[2:]

        #my_df = my_df.iloc[:, 2:]
        figs = []
        for col in range(len(away_team)):
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=list(away_name),
                x=[away_team[col]],
                showlegend=True,
                text='test',
                textposition='inside',
                name=f'{away_name}',
                orientation='h'
            ))   

            fig.add_trace(go.Bar(
                y=list(home_name),
                x=[home_team[col]],
                text='test',
                textposition='inside',
                name=f'{home_name}',
                orientation='h'
            ))

            fig.update_layout(
                title={
                    'text':f'{header[col]}',
                    'font':{
                            'family': 'sans-serif',
                            'size': 14,
                            },
                },
                xaxis_title='',
                yaxis_title='',
                barmode='stack',
                showlegend=False,
                width=800,
                height=150,
                margin=dict(l=0, r=0, t=80, b=0),
                xaxis=dict(showticklabels=False),
            )
            figs.append(fig)
        return figs
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
    
    # def get_match_statss(self, team1_id, team2_id):    
    #     sql_query = f"""
    #         SELECT mi.*
    #         FROM match_stats mi
    #         WHERE mi.team_id = ? OR mi.team_id = ?
    #     """
    #     param_1 = team1_id
    #     param_2 = team2_id

    #     df = pd.read_sql(sql_query, self.conn, params=[param_1, param_2])
    #     df = df[df.groupby('match_id')['team_id'].transform('nunique') == 2]
    #     return df, df['match_id'].unique().tolist()
    
    def get_match_stats(self, team_id1: str, team_id2: str):
        sql_query = """
            SELECT ms.match_id, ms.team_id, ms.fgm, ms.fga, ms.tpm, ms.tpa, ms.ftm, ms.fta, ms.oreb, ms.dreb, ms.reb, 
            ms.ast, ms.tov, ms.stl, ms.blk, pf, mi.pts
            FROM match_stats ms
            JOIN match_info mi ON ms.match_id = mi.match_id
            WHERE (ms.team_id = ? AND mi.team_id = ?) OR (ms.team_id = ? AND mi.team_id = ?)
        """
        params = [team_id1, team_id1, team_id2, team_id2]

        df = pd.read_sql(sql_query, self.conn, params=params)
        df = df[df.groupby('match_id')['team_id'].transform('nunique') == 2]
        
        return df, df['match_id'].unique().tolist()