import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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
    
    def create_bar(self, stats1, stats2, home: bool, title: str, title2: str):
        if home:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[stats1],
                y=[0],
                name=f'{title}',
                orientation='h',
                marker=dict(color='#50e991')

            ))
            fig.add_trace(go.Bar(
                x=[stats2-stats1],
                y=[0],
                name=f'{title2}',
                orientation='h',
                marker=dict(color='#474440')
            ))

            fig.update_layout(
                barmode="stack",
                yaxis=dict(visible=False, showticklabels=False),
                xaxis=dict(
                    range=[0, stats2],
                    visible=False,
                    showticklabels=False,
                    showgrid=False,
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                height=50,
            )
        else:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[stats1],
                y=[0],
                orientation='h',
                name=f'{title}',
                marker=dict(color='#0bb4ff')
            ))

            fig.add_trace(go.Bar(
                x=[stats2 - stats1],
                y=[0],
                name=f'{title2}',
                orientation='h',
                marker=dict(color='#474440')
            ))

            fig.update_layout(
        barmode="stack",
        yaxis=dict(visible=False, showticklabels=False),
        xaxis=dict(
            range=[stats2, 0],
            visible=False,
            showticklabels=False,
            showgrid=False,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=50,
    )
        return fig



    
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
    
    def get_match_stats(self, team_id1: str, team_id2: str):
        sql_query = """
            SELECT ms.match_id, ms.team_id, ti.team_name, ms.fgm, ms.fga, ms.tpm, ms.tpa, ms.ftm, ms.fta, ms.oreb, ms.dreb, 
            ms.reb, ms.ast, ms.tov, ms.stl, ms.blk, pf, mi.pts
            FROM match_stats ms
            JOIN match_info mi ON ms.match_id = mi.match_id
            JOIN team_info ti ON ms.team_id = ti.team_id
            WHERE (ms.team_id = ? AND mi.team_id = ?) OR (ms.team_id = ? AND mi.team_id = ?)
        """
        params = [team_id1, team_id1, team_id2, team_id2]

        df = pd.read_sql(sql_query, self.conn, params=params)
        df = df[df.groupby('match_id')['team_id'].transform('nunique') == 2]
        
        return df, df['match_id'].unique().tolist()
    def get_match_statss(self, team_id1: str, team_id2: str):
        sql_query = """
            SELECT ms.match_id, ms.team_id, ti.team_name, ms.fgm, ms.fga, ms.tpm, ms.tpa, ms.ftm, ms.fta, ms.oreb, ms.dreb, ms.reb, 
            ms.ast, ms.tov, ms.stl, ms.blk, pf, mi.pts
            FROM match_stats ms
            JOIN match_info mi ON ms.match_id = mi.match_id
            JOIN team_info ti on ms.match_id = ti.team_id

            WHERE (ms.team_id = ? AND mi.team_id = ?) OR (ms.team_id = ? AND mi.team_id = ?)
        """
        params = [team_id1, team_id1, team_id2, team_id2]

        df = pd.read_sql(sql_query, self.conn, params=params)
        df = df[df.groupby('match_id')['team_id'].transform('nunique') == 2]
        
        return df, df['match_id'].unique().tolist()