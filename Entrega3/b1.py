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

# Crear la conexión a la base de datos
conn = psy2.connect(dbname=dbname, user=user, password=password, host=host)

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

# Crear un DataFrame con los resultados de la consulta
df_typeshooter = pd.read_sql(sql_query_typeshooter, conn)

# Crear un DataFrame con los resultados de la consulta
df_shootingtype = pd.read_sql(sql_query_shootingtype, conn)

# Crear la aplicación Dash
app = dash.Dash(__name__)


# Diseñar el diseño de la aplicación
app.layout = html.Div([
    html.H1('Distribución de Tipos de Tiroteos', style={'text-align': 'center'}),
    
    # Gráfico de dispersión para 'shooting_type'
    dcc.Graph(
        id='shooting-type-scatter-plot',
        figure=px.scatter(df_shootingtype, x='shooting_type', y='count', title='Distribución de Tipos de Tiroteos').update_layout(
            xaxis_title='Tipo de Tiroteo',
            yaxis_title='Conteo'
        )
    ),
    
    # Gráfico de torta para 'gender_shooter1'
    dcc.Graph(
        id='gender-shooter-pie-chart',
        figure=px.pie(df_typeshooter, names='gender_shooter1', title='Distribución de Género de Tiradores')
    ),

    # Gráfico de barras para 'shooter_relationship1'
    dcc.Graph(
        id='relationship-bar-chart',
        figure=px.bar(df_typeshooter, x='shooter_relationship1', y='count_relationship', title='Distribución de Relaciones de Tiradores')
    )
])




# Cerrar la conexión a la base de datos
conn.close()

# Iniciar la aplicación Dash
if __name__ == '__main__':
    app.run_server(port=8085)
