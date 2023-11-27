import pandas as pd
import psycopg2 as psy2
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from sqlalchemy import create_engine

import plotly.graph_objects as go
from dash import Dash, Input, Output


dbname = "school-shootings-data"
user = "postgres"
password = "123456789"
host = "localhost"


conn = psy2.connect(dbname =dbname, user = user, password = password, host = host)

sql_query = "select lat, long from shooterincidentlocation;"

#select state, count(state) from state as st natural join district_info group by state;
df =pd.read_sql(sql_query, conn)

#print (df.iloc[0:9])

print (df[['lat','long']].iloc[0:50])


app = Dash(__name__)

fig = go.Figure(data=go.Scattergeo(
lon = df['long'],
lat = df['lat'],
mode = 'markers',
))

fig.update_layout(
title = 'Coornedanas de los Tiroteos',
geo_scope='usa',
)
fig.show()

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(port=8085)
