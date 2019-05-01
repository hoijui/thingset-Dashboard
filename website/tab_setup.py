# -*- coding: utf-8 -*-

import dash_html_components as html
import dash_daq as daq

def content():
    return html.Div([
        html.Div([
            daq.NumericInput(
                id='my-numeric-input',
                label='Battery max. voltage',
                value=0,
                style={'padding': '20px 0px 20px 0px'}
            ),
            html.Div(id='numeric-input-output'),
            html.Div([
                daq.BooleanSwitch(
                    id='my-daq-booleanswitch',
                    label='DCDC enabled',
                    on=True
                )],
                style={'padding': '20px 0px 20px 0px'}
            ),
            html.Div(id='output-boolean', style={'align':'center'}),
        ], className="six columns"),
        html.Div([
            daq.NumericInput(
                id='my-numeric-input',
                label='Battery max. current',
                value=0,
                style={'padding': '20px 0px 20px 0px'}
            ),
            html.Div(id='numeric-input-output'),
        ], className="six columns"),
    ], className="row")


