# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def db_connect():
    now = datetime.now()
    con = sqlite3.connect("data/test0530.db")
    df = pd.read_sql_query("SELECT * from ThingSet " \
        "where time >= datetime('{}');".format(now-timedelta(minutes=10)), con=con)
    return df

def content():
    df = db_connect()
    meas = list(df.columns.values)
    opt = [dict(label=item, value=item) for item in meas]

    return html.Div([
        dcc.Dropdown(
            id='data-sel-1',
            options=opt,
            multi=True,
            style={'padding':'0px 10px 0px 10px', 'width':'600px'}
        ),
        dcc.Graph(
            id='graph-1',
            style={'padding': '0px 10px 15px 10px'},
        ),

        dcc.Interval(
            id='live-data-update',
            interval=2000,
            disabled=False,
            n_intervals=0
        ),

        dcc.Dropdown(
            id='data-sel-2',
            options=opt,
            multi=True,
            style={'padding':'0px 10px 0px 10px', 'width':'600px'}
        ),
        dcc.Graph(
            id='graph-2',
            style={'padding': '20px 0px 20px 0px'},
        ),
    ],
        style={'width': '1200px', 'margin-left':'auto', 'margin-right':'auto'})

def gen_livegraph1(app):
    @app.callback(Output('graph-1', 'figure'), [Input('live-data-update', 'n_intervals'), Input('data-sel-1', 'value')])
    def gen_live_data(interval, selected_value):
        now = datetime.now()
        df = db_connect()
        return {
            'data': [{
                'x': df['time'],
                'y': df[value],
                'name': value,
                'line': {
                    'width': 3,
                    'shape': 'linear'
                }
            } for value in selected_value]
        }

    @app.callback(Output('live-data-update', 'max_intervals'), [Input('graph-1', 'relayoutData')])
    def stop_interval(relayoutData):
        print("FIRE")
        if not ('xaxis.autorange' or 'autosize') in relayoutData:
            print("STOP")
            return 0
        else:
            print("START")
            return -1

def gen_livegraph2(app):
    @app.callback(Output('graph-2', 'figure'), [Input('live-data-update', 'n_intervals'), Input('data-sel-2', 'value')])
    def gen_live_data(interval, selected_value):
        now = datetime.now()
        df = db_connect()
        return {
            'data': [{
                'x': df['time'],
                'y': df[value],
                'name': value,
                'line': {
                    'width': 3,
                    'shape': 'linear'
                }
            } for value in selected_value],
            'layout': {
                'clickmode': 'event+select'
            }
        }
