import sqlite3
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import website.tab_setup, website.tab_graphs, website.tab_dashboard

def create_app():
    """
    Create Dash app. Add config parameters here.
    """
    app = dash.Dash('Solarbox')
    app.config['suppress_callback_exceptions'] = True
    app.layout = html.Div(children=[
        #html.H1(children='Libre Solar ThingSet Interface')])
        dcc.Tabs(id="tabs-example", value='tab-dashboard', children=[
            dcc.Tab(label='Dashboard', value='tab-dashboard'),
            dcc.Tab(label='Graphs', value='tab-graphs'),
            dcc.Tab(label='Setup', value='tab-setup'),
        ], style={'padding': '20px 0px 20px 0px'}),
        html.Div(id='tabs-content')
    ], className="container")

    @app.callback(Output('tabs-content', 'children'),
                [Input('tabs-example', 'value')])
    def render_content(tab):
        if tab == 'tab-graphs':
            return website.tab_graphs.content()
        elif tab == 'tab-dashboard':
            return website.tab_dashboard.content()
        elif tab == 'tab-setup':
            return website.tab_setup.content()

    website.tab_graphs.gen_livegraph1(app)
    website.tab_graphs.gen_livegraph2(app)

    return app
