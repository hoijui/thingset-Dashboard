# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

con = sqlite3.connect("data/solarbox.db")
df = pd.read_sql_query("SELECT * from Solarbox;", con)
meas = list(df.columns.values)
meas.remove('index')
opt = [dict(label=item, value=item) for item in meas]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='LibreSolar Data Visualization'),
    html.Div('Choose a value to display'),
    dcc.Dropdown(
        id='meas-dropdown',
        options=opt,
        multi=True
    ),
    dcc.Graph(id='solarbox'),
    html.Div([
        daq.BooleanSwitch(
            id='my-daq-booleanswitch',
            label='Send boolean value',
            on=True
        )],
        style={'padding': '20px 0px 20px 0px'}
    ),
    html.Div(id='output-boolean', style={'align':'center'}),
    daq.NumericInput(
        id='my-numeric-input',
        label='Set numeric value',
        value=0,
        style={'padding': '20px 0px 20px 0px'}
    ),
    html.Div(id='numeric-input-output')
], className="container")

@app.callback(
    dash.dependencies.Output('output-boolean', 'children'),
    [dash.dependencies.Input('my-daq-booleanswitch', 'on')])
def update_output_switch(on):
    print(str(on))
    return 'The switch is {}.'.format(on)

@app.callback(
    dash.dependencies.Output('numeric-input-output', 'children'),
    [dash.dependencies.Input('my-numeric-input', 'value')])
def update_output(value):
    return 'The value is {}.'.format(value)

@app.callback(Output('solarbox', 'figure'),
              [Input('meas-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    if not selected_dropdown_value:
        pass
    else:
        return {
            'data': [{ 
                'x': df.index,
                'y': df[value],
                'line': {
                    'width': 3,
                    'shape': 'spline'
                }
            } for value in selected_dropdown_value],
            'layout': {
                'margin': {
                    'l': 100,
                    'r': 100,
                    'b': 30,
                    't': 30
                }
            }
        }
if __name__ == '__main__':
    app.run_server(debug=True)