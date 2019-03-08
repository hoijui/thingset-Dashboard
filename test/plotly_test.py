import plotly.plotly as py
import plotly.graph_objs as go 
import pandas as pd
import sqlite3

con = sqlite3.connect("../data/solarbox.db")
df = pd.read_sql_query("SELECT timestamp, vBat, vSolar from Solarbox;", con)

trace = go.Scatter(
    x = df['timestamp'],
    y = df['vSolar']
)

data = [trace]
py.iplot(data)