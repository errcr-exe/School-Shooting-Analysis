import pandas as pd
import psycopg2 as psy2
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


dbname = "school-shootings-data"
user = "postgres"
password = "123456789"
host = "localhost"



conn = psy2.connect(dbname =dbname, user = user, password = password, host = host)

sql_query = "select w.weapon as weapon, count(w.weapon) as count from weapon as w join shooterweapon as sw on w.uid = sw.weapon_uid join shootingincident as si on sw.uid_incident = si.uid group by (w.weapon) order by (count(w.weapon)) desc"
df =pd.read_sql(sql_query, conn)

#print (df.iloc[0:9])

print (df[['weapon','count']].iloc[0:7])

app =dash.Dash()
app.layout = html.Div([
html.H1('Graficas', style={'text-align' : 'center'}),
html.Div('El impacto del uso de armas de familiares en los tiroteos y la relación con el fácil acceso a armas en Estados Unidos'),
dcc.Graph(
id = 'sample-graph',
figure = px.bar(df[['weapon','count']].iloc[0:8], x='weapon', y='count', title='Fuente').update_layout(
xaxis_title = 'Arma',
yaxis_title = 'Conteo'
)

)
])


conn.close()


# Ejecución de la aplicación
if __name__ == '__main__':
    app.run_server(port=8085, debug=True)