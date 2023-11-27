import pandas as pd
import psycopg2 as psy2
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from sqlalchemy import create_engine

dbname = "school-shootings-data"
user = "postgres"
password = "123456789"
host = "localhost"

conn = psy2.connect(dbname =dbname, user = user, password = password, host = host)

sql_query = "select state, count(state) from state as st natural join district_info group by state;"


df =pd.read_sql(sql_query, conn)


print (df[['state','count']].iloc[0:47])

app =dash.Dash()
app.layout = html.Div([
html.H1('Graficas', style={'text-align' : 'center'}),
html.Div('- Investigar en que estados, ciudades e instituciones es más probable que ocurran tiroteos, con el fin de encontrar los lugares más propensos y así las autoridades puedan tomar medidas adicionales para evitar este tipo de tragedias'),
dcc.Graph(
id = 'sample-graph',
figure = px.bar(df[['state','count']].iloc[0:47], x='state', y='count', title='Estados').update_layout(
xaxis_title = 'Estado',
yaxis_title = 'Conteo'
)

)
])


conn.close()

if __name__ == '__main__':
    app.run(port=8085)
