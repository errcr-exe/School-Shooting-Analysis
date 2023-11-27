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

# Función para obtener datos de la base de datos
def get_data(sql_query):
    conn = psy2.connect(dbname=dbname, user=user, password=password, host=host)
    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df

# Consulta SQL para obtener datos sobre la edad
sql_query_age = "select age_shooter1, count(age_shooter1) from ShooterIncidentRelation as sir join Typeshooter as ts on sir.typeshooter1_uid = ts.uid group by ts.age_shooter1 order by (age_shooter1);"
df_age = get_data(sql_query_age)

# Consulta SQL para obtener datos sobre la raza
sql_query_race = "select race_ethnicity_shooter1, count(race_ethnicity_shooter1) from ShooterIncidentRelation as sir join Typeshooter as ts on sir.typeshooter1_uid = ts.uid group by ts.race_ethnicity_shooter1 order by (race_ethnicity_shooter1);"
df_race = get_data(sql_query_race)

# Creación de la aplicación Dash
app = dash.Dash(__name__)

# Diseño de la aplicación
app.layout = html.Div([
    html.H1('Análisis de Tiroteos Escolares', style={'text-align': 'center'}),
    
    dcc.Tabs([
        dcc.Tab(label='Edad', children=[
            html.Div([
                dcc.Graph(
                    id='age-graph',
                    figure=px.line(df_age[['age_shooter1', 'count']].iloc[0:42], x='age_shooter1', y='count', title='Edad').update_layout(
                        xaxis_title='Edad',
                        yaxis_title='Conteo'
                    )
                )
            ])
        ]),
        
        dcc.Tab(label='Raza', children=[
            html.Div([
                dcc.Graph(
                    id='race-graph',
                    figure=px.bar(df_race[['race_ethnicity_shooter1', 'count']].iloc[0:8], x='race_ethnicity_shooter1', y='count', title='Raza').update_layout(
                        xaxis_title='Raza',
                        yaxis_title='Conteo'
                    )
                )
            ])
        ]),
    ])
])

# Ejecución de la aplicación
if __name__ == '__main__':
    app.run_server(port=8085, debug=True)
