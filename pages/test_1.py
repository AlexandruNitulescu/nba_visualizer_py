import plotly.express as px
import streamlit as st
import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
import modules.helper_functions as hlp
import plotly.graph_objects as go
import  streamlit_toggle as tog

col_1, col_2 = st.columns(2)
def create_cols():
    fig = go.Figure()
    percentage = 0.6
    fig.add_trace(go.Bar(
        x=[percentage],
        y=[0],
        orientation='h',
        marker=dict(color='green')
    ))

    fig.add_trace(go.Bar(
        x=[1 - percentage],
        y=[0],
        orientation='h',
        marker=dict(color='grey')
    ))

    fig.update_layout(
        barmode="stack",
        yaxis=dict(visible=False, showticklabels=False),
        xaxis=dict(
            range=[1, 0],
            visible=False,
            showticklabels=False,
            showgrid=False,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=50,
    )
    col_1.plotly_chart(fig, use_container_width=True)
    fig = go.Figure()

    percentage = 0.4

    fig.add_trace(go.Bar(
        x=[percentage],
        y=[0],
        orientation='h',
        marker=dict(color='green')
    ))

    fig.add_trace(go.Bar(
        x=[1 - percentage],
        y=[0],
        orientation='h',
        marker=dict(color='grey')
    ))

    fig.update_layout(
        barmode="stack",
        yaxis=dict(visible=False, showticklabels=False),
        xaxis=dict(
            range=[0, 1],
            visible=False,
            showticklabels=False,
            showgrid=False,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=50,
    )
    col_2.plotly_chart(fig, use_container_width=True)

create_cols()    