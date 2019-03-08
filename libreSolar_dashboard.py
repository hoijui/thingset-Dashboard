#!/usr/bin/env python
"""Dashboard for Libre Solar box. Reads data from sqlite database
and plots live data at http://localhost:8050"""
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    'libreSolar-dashboard',
    external_stylesheets=external_css
)
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1("Libre Solar Data Visualization Dashboard")
    ], className='top-title'),
    html.Div([
        html.Div([
            html.H3("Live Data")
        ], className='live-title'),
        html.Div([
            dcc.Graph(id='live-data'),
        ], className='live-data-graph'),
        dcc.Interval(id='live-data-update', interval=1000, n_intervals=0)
    ], className='row live-data-graph')
], style={'padding': '0px 10px 15px 10px',
          'margin-left': 'auto', 'margin-right': 'auto', 'width': '900px'})

@app.callback(Output('live-data', 'figure'), [Input('live-data-update', 'n_intervals')])
def gen_live_data(interval):
    now = datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour

    total_time = (hour*3600) + (minute*60) + sec
    con = sqlite3.connect("data/solarbox.db")
    data_frame = pd.read_sql_query("SELECT * from Solarbox " \
        "where time >= datetime('{}');".format(now-timedelta(minutes=1)), con=con)

if __name__ == '__main__':
    app.run_server(debug=True)
