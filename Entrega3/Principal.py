import pandas as pd
import psycopg2 as psy2
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from sqlalchemy import create_engine
import plotly.graph_objects as go
from dash import Dash, Input, Output

# Conexión a la base de datos
dbname = "school-shootings-data"
user = "postgres"
password = "123456789"
host = "localhost"

conn = psy2.connect(dbname=dbname, user=user, password=password, host=host)

# Consulta SQL para obtener datos de ShooterIncidentRelation
sql_query_age = "select age_shooter1, count(age_shooter1) from ShooterIncidentRelation as sir join Typeshooter as ts on sir.typeshooter1_uid = ts.uid group by ts.age_shooter1 order by (age_shooter1);"
df_age = pd.read_sql(sql_query_age, conn)

# Consulta SQL para obtener datos de TypeShooter
sql_query_typeshooter = """
    SELECT age_shooter1, gender_shooter1, race_ethnicity_shooter1, shooter_relationship1, shooter_deceased1, deceased_notes1
    FROM TypeShooter;
"""
df_typeshooter = pd.read_sql(sql_query_typeshooter, conn)

# Consulta SQL para obtener la distribución de tipos de tiroteos
sql_query_shootingtype = """
SELECT st.shooting_type, COUNT(*) as count
FROM ShootingIncident si
JOIN ShootingType st ON si.uid_shooting_type = st.uid
GROUP BY st.shooting_type
ORDER BY count DESC;
"""

# Consulta SQL para obtener la distribución del género y la relación del tirador
sql_query_typeshooter = """
    SELECT gender_shooter1, COUNT(gender_shooter1) as count_gender,
           shooter_relationship1, COUNT(shooter_relationship1) as count_relationship
    FROM TypeShooter
    GROUP BY gender_shooter1, shooter_relationship1
"""

# Consulta SQL para obtener la distribución de la fuente del arma
sql_query_weapon_source = "select ws.weapon_source as weapon_source, count(ws.weapon_source) as count from weapon_source as ws join shooterweapon as sw on ws.uid = sw.weapon_source_uid join shootingincident as si on sw.uid_incident = si.uid group by (ws.weapon_source) order by (count(ws.weapon_source)) desc;"
df_weapon_source = pd.read_sql(sql_query_weapon_source, conn)

# Consulta SQL para obtener la distribución del tipo de arma
sql_query_weapon = "select w.weapon as weapon, count(w.weapon) as count from weapon as w join shooterweapon as sw on w.uid = sw.weapon_uid join shootingincident as si on sw.uid_incident = si.uid group by (w.weapon) order by (count(w.weapon)) desc"
df_weapon = pd.read_sql(sql_query_weapon, conn)

# Consulta SQL para obtener la distribución del lugar
sql_query_state = "select state, count(state) from state as st natural join district_info group by state;"
df_state = pd.read_sql(sql_query_state, conn)

# Consulta SQL para obtener las coordenadas de los tiroteos
sql_query_coordinates = "select lat, long from shooterincidentlocation;"
df_coordinates = pd.read_sql(sql_query_coordinates, conn)

def get_data(sql_query):
    conn = psy2.connect(dbname=dbname, user=user, password=password, host=host)
    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df

# Crear un DataFrame con los resultados de las consultas
df_shootingtype = pd.read_sql(sql_query_shootingtype, conn)
df_typeshooter = pd.read_sql(sql_query_typeshooter, conn)

sql_query_race = "select race_ethnicity_shooter1, count(race_ethnicity_shooter1) from ShooterIncidentRelation as sir join Typeshooter as ts on sir.typeshooter1_uid = ts.uid group by ts.race_ethnicity_shooter1 order by (race_ethnicity_shooter1);"
df_race = get_data(sql_query_race)

# Cerrar la conexión a la base de datos
conn.close()

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Diseño de la aplicación
app.layout = html.Div([
    html.H1('Análisis de Tiroteos en Escuelas', style={'text-align': 'center'}),

    
    dcc.Tabs([
        dcc.Tab(label='Distribución de Edad de los Tiradores', children=[
            dcc.Graph(
                id='age-distribution-line-plot',
                figure=px.line(df_age[['age_shooter1', 'count']].iloc[0:42], x='age_shooter1', y='count', title='Distribución de Edad de los Tiradores').update_layout(
                    xaxis_title='Edad',
                    yaxis_title='Conteo'
                )
            ),
            dcc.Graph(
                id='race-graph',
                figure=px.bar(df_race[['race_ethnicity_shooter1', 'count']].iloc[0:8], x='race_ethnicity_shooter1', y='count', title='Raza').update_layout(
                    xaxis_title='Raza',
                    yaxis_title='Conteo'
                )
            )
        ]),
        
        dcc.Tab(label='Distribución de Tipos de Tiroteos', children=[
            dcc.Graph(
                id='shooting-type-scatter-plot',
                figure=px.scatter(df_shootingtype, x='shooting_type', y='count', title='Distribución de Tipos de Tiroteos').update_layout(
                    xaxis_title='Tipo de Tiroteo',
                    yaxis_title='Conteo'
                )
            )
        ]),
        
        dcc.Tab(label='Distribución de Género y Relaciones de Tiradores', children=[
            dcc.Graph(
                id='gender-shooter-pie-chart',
                figure=px.pie(df_typeshooter, names='gender_shooter1', title='Distribución de Género de Tiradores')
            ),
            dcc.Graph(
                id='relationship-bar-chart',
                figure=px.bar(df_typeshooter, x='shooter_relationship1', y='count_relationship', title='Distribución de Relaciones de Tiradores')
            )
        ]),

        dcc.Tab(label='Distribución de la Fuente y el tipo de Arma', children=[
            dcc.Graph(
                id='weapon-source-histogram',
                figure=px.histogram(df_weapon_source[['weapon_source', 'count']].iloc[0:8], x='weapon_source', y='count', title='Fuente del Arma').update_layout(
                    xaxis_title='Fuente del Arma',
                    yaxis_title='Conteo'
                )
            ),
            dcc.Graph(
                id='weapon-histogram',
                figure=px.bar(df_weapon[['weapon', 'count']].iloc[0:8], x='weapon', y='count', title='Tipo de Arma').update_layout(
                    xaxis_title='Arma',
                    yaxis_title='Conteo'
                )
            )
        ]),
        
        dcc.Tab(label='Distribución del Lugar de los incidentes', children=[ 
            dcc.Graph(
                id='state-bar-chart',
                figure=px.bar(df_state[['state', 'count']].iloc[0:47], x='state', y='count', title='Estados').update_layout(
                    xaxis_title='Estado',
                    yaxis_title='Conteo'
                )
            ),
            dcc.Graph(
                id='coordinates-map',
                figure=go.Figure(data=go.Scattergeo(
                    lon=df_coordinates['long'],
                    lat=df_coordinates['lat'],
                    mode='markers',
                )).update_layout(
                    title='Coordenadas de los Tiroteos',
                    geo_scope='usa',
                )
            ),
        ]),
    ])
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(port=8085)






