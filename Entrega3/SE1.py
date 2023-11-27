import pandas as pd
import psycopg2 as psy2
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from sqlalchemy import create_engine
from dash.dependencies import Input, Output

# Conexión a la base de datos
dbname = "school-shootings-data"
user = "postgres"
password = "123456789"
host = "localhost"


conn = psy2.connect(dbname =dbname, user = user, password = password, host = host)

sql_query = "select ws.weapon_source as weapon_source, count(ws.weapon_source) as count from weapon_source as ws join shooterweapon as sw on ws.uid = sw.weapon_source_uid join shootingincident as si on sw.uid_incident = si.uid group by (ws.weapon_source) order by (count(ws.weapon_source)) desc;"
df =pd.read_sql(sql_query, conn)


print (df[['weapon_source','count']].iloc[0:7])

app =dash.Dash()
app.layout = html.Div([
html.H1('Graficas', style={'text-align' : 'center'}),
html.Div('El impacto del uso de armas de familiares en los tiroteos y la relación con el fácil acceso a armas en Estados Unidos'),
dcc.Graph(
id = 'sample-graph',
figure = px.histogram(df[['weapon_source','count']].iloc[0:8], x='weapon_source', y='count', title='Fuente').update_layout(
xaxis_title = 'Fuente del Arma',
yaxis_title = 'Conteo'
)

)
])

conn.close()
# Ejecución de la aplicación
if __name__ == '__main__':
    app.run_server(port=8085, debug=True)

