# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def content():
    return html.Div([
        dcc.Dropdown(
            id='data-sel-1',
            multi=True,
            style={'padding':'0px 10px 0px 10px', 'width':'600px'}
        ),
        dcc.Graph(
            id='graph-1',
            style={'padding': '0px 10px 15px 10px'},
        ),

        dcc.Interval(
            id='live-data-update',
            interval=1000,
            n_intervals=0
        ),

        dcc.Dropdown(
            id='data-sel-2',
            multi=True,
        ),
        dcc.Graph(
            id='graph-2',
            style={'padding': '20px 0px 20px 0px'},
        ),
    ],
        style={'width': '1200px', 'margin-left':'auto', 'margin-right':'auto'})

def gen_livegraph(app):
    @app.callback(Output('graph-1', 'figure'), [Input('live-data-update', 'n_intervals')])
    def gen_live_data(interval):
        now = datetime.now()
        sec = now.second
        minute = now.minute
        hour = now.hour
 
        total_time = (hour*3600) + (minute*60) + sec
        con = sqlite3.connect("data/livetest.db")
        df = pd.read_sql_query("SELECT * from ThingSet " \
            "where time >= datetime('{}');".format(now-timedelta(minutes=10)), con=con)
        return {
            'data': [{
                'x': df['time'],
                'y': df['Load_A'],
                'name': 'Load_A',
                'line': {
                    'width': 3,
                    'shape': 'spline'
                }
            }]
        }
