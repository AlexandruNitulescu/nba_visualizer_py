import streamlit as st
import pandas as pd
import plotly.express as px
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
placeholder = st.empty()
placeholder_1 = st.empty()

col3, col4 = st.columns(2)

team_ppg = pd.read_sql('''
    SELECT t.team_name, AVG(mi.pts) as ppg
    FROM team_info t
    JOIN match_info mi ON t.team_id = mi.team_id
    GROUP BY t.team_name
    ORDER BY ppg DESC
''', conn)

team_astpg = pd.read_sql('''
    SELECT t.team_name, AVG(mi.ast) as avg_ast
    FROM team_info t
    JOIN match_stats mi ON t.team_id = mi.team_id
    GROUP BY t.team_name
    ORDER BY ast DESC
''', conn)
avg_ppg = team_ppg['ppg'].mean()


col1.header("# NBA Team Average Stats")
col1.markdown("Description: The following metrics show the average performance of NBA teams in terms of points, assists, rebounds, steals, blocks, turnovers, and personal fouls during the current 2022-23 season.")
mean_values = calc.calculate_mean_values()
metric_1.metric(label="Average Points per game", value=mean_values['avg_pts'][0])
metric_2.metric(label="Average Points per game", value=mean_values['avg_ast'][0])
metric_3.metric(label="Average Points per game", value=mean_values['avg_reb'][0])
metric_4.metric(label="Average Points per game", value=mean_values['avg_stl'][0])
metric_5.metric(label="Average Points per game", value=mean_values['avg_blk'][0])
metric_6.metric(label="Average Points per game", value=mean_values['avg_tov'][0])
metric_7.metric(label="Average Points per game", value=mean_values['avg_pf'][0])
style_metric_cards()


subtab_avg_pts, subtab_avg_ast, subtab_avg_reb = placeholder.tabs(['**AVG PPG**', '**AVG AST**', '**AVG REB**'])
with subtab_avg_pts:
    st.header("AVG")
    fig = px.bar(team_ppg, y='team_name', x='ppg', orientation='h',
             color =['#ffa600' if ppg >= avg_ppg else '#ff6361' for ppg in team_ppg['ppg']],
             height=600, width=800)

    fig.update_layout(title='Average Points per Game (NBA 2022-23)',
                      xaxis_title='PPG',
                      yaxis_title='',
                      xaxis_tickformat='.1f',
                      yaxis_autorange='reversed',
                      xaxis_range=[108, 122],
                      xaxis_showgrid=True,
                      xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
                      xaxis_ticks='outside',
                      yaxis_showgrid=False,
                      font=dict(size=12))

    fig.add_shape(type='line', x0=avg_ppg, y0=0, x1=avg_ppg, y1=len(team_ppg),
              line=dict(color='black', dash='dash'))

    st.plotly_chart(fig, use_container_width=True)
with subtab_avg_ast:
    st.header("AST")
    fig = px.bar(team_astpg, y='team_name', x='avg_ast', orientation='h',
             color =['#ffa600' if ast >= avg_ast else '#ff6361' for ast in team_astpg['avg_ast']],
             height=600, width=800)

    fig.update_layout(title='Average Assists per Game (NBA 2022-23)',
                      xaxis_title='AST',
                      yaxis_title='',
                      xaxis_tickformat='.1f',
                      yaxis_autorange='reversed',
                      xaxis_showgrid=True,
                      xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
                      xaxis_ticks='outside',
                      yaxis_showgrid=False,
                      font=dict(size=12))

    fig.add_shape(type='line', x0=avg_ppg, y0=0, x1=avg_ppg, y1=len(team_ppg),
              line=dict(color='black', dash='dash'))

    placeholder_1.plotly_chart(fig, use_container_width=True)   


####################

df = px.data.gapminder().query("continent == 'Europe'")
fig = px.bar(df, x='year', y='pop',
             hover_data=['lifeExp', 'gdpPercap'], color='country',
             labels={'pop':'population of Canada'}, height=600, width=800)

fig.update_layout(title='Team wins and loses',
                  xaxis_title='PPG',
                  yaxis_title='',
                  xaxis_gridcolor='rgba(0, 0, 0, 0.4)', 
                  font=dict(size=12))
st.plotly_chart(fig, use_container_width=True)

df = px.data.election()
geojson = px.data.election_geojson()

fig = px.choropleth_mapbox(df, geojson=geojson, color="Bergeron",
                           locations="district", featureidkey="properties.district",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="carto-positron", zoom=9)
col3.plotly_chart(fig, use_container_width=True)

df = px.data.tips()
fig = px.scatter(df, x="total_bill", y="tip", color="smoker", facet_col="sex", facet_row="time")
col4.plotly_chart(fig, use_container_width=True)

colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']

fig = go.Figure(data=[go.Pie(labels=['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen'],
                             values=[4500,2500,1053,500])])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
col3.plotly_chart(fig, use_container_width=True)

df = px.data.gapminder().query("year == 2007")
fig = px.icicle(df, path=[px.Constant('world'), 'continent', 'country'], values='pop',
                  color='lifeExp', hover_data=['iso_alpha'])
col4.plotly_chart(fig, use_container_width=True)

df = px.data.election()
fig = px.scatter_ternary(df, a="Joly", b="Coderre", c="Bergeron", color="winner", size="total", hover_name="district",
                   size_max=15, color_discrete_map = {"Joly": "blue", "Bergeron": "green", "Coderre":"red"} )
col3.plotly_chart(fig, use_container_width=True)

import plotly.figure_factory as ff

# Add table data
table_data = [['Team', 'Wins', 'Losses', 'Ties'],
              ['Montréal<br>Canadiens', 18, 4, 0],
              ['Dallas Stars', 18, 5, 0],
              ['NY Rangers', 16, 5, 0],
              ['Boston<br>Bruins', 13, 8, 0],
              ['Chicago<br>Blackhawks', 13, 8, 0],
              ['Ottawa<br>Senators', 12, 5, 0]]

# Initialize a figure with ff.create_table(table_data)
fig = ff.create_table(table_data, height_constant=60)

# Add graph data
teams = ['Montréal Canadiens', 'Dallas Stars', 'NY Rangers',
         'Boston Bruins', 'Chicago Blackhawks', 'Ottawa Senators']
GFPG = [3.54, 3.48, 3.0, 3.27, 2.83, 3.18]
GAPG = [2.17, 2.57, 2.0, 2.91, 2.57, 2.77]

# Make traces for graph
trace1 = go.Bar(x=teams, y=GFPG, xaxis='x2', yaxis='y2',
                marker=dict(color='#0099ff'),
                name='Goals For<br>Per Game')
trace2 = go.Bar(x=teams, y=GAPG, xaxis='x2', yaxis='y2',
                marker=dict(color='#404040'),
                name='Goals Against<br>Per Game')

# Add trace data to figure
fig.add_traces([trace1, trace2])
# initialize xaxis2 and yaxis2
fig['layout']['xaxis2'] = {}
fig['layout']['yaxis2'] = {}

# Edit layout for subplots
fig.layout.yaxis.update({'domain': [0, .45]})
fig.layout.yaxis2.update({'domain': [.6, 1]})

# The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
fig.layout.yaxis2.update({'anchor': 'x2'})
fig.layout.xaxis2.update({'anchor': 'y2'})
fig.layout.yaxis2.update({'title': 'Goals'})

# Update the margins to add a title and see graph x-labels.
fig.layout.margin.update({'t':75, 'l':50})
fig.layout.update({'title': '2016 Hockey Stats'})

# Update the height because adding a graph vertically will interact with
# the plot height calculated for the table
fig.layout.update({'height':800})
col3.plotly_chart(fig, use_container_width=True)
