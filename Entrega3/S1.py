# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 15:26:57 2023

@author: usuario
"""
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

sql_query = "select age_shooter1, count(age_shooter1) from ShooterIncidentRelation as sir join Typeshooter as ts on sir.typeshooter1_uid = ts.uid group by ts.age_shooter1 order by (age_shooter1);"


df =pd.read_sql(sql_query, conn)

#print (df.iloc[0:9])

print (df[['age_shooter1','count']].iloc[0:42])

app =dash.Dash()
app.layout = html.Div([
    html.H1('Graficas', style={'text-align' : 'center'}),
    html.Div('- Investigar las características de los perpetradores, como su edad, género, antecedentes de salud mental, armas utilizadas, relación con la víctima e historial de comportamiento puede ser fundamental para comprender las causas de los tiroteos en escuelas y desarrollar estrategias de prevención. Estos perfiles pueden ser utilizados por autoridades y profesionales para tomar medidas y mitigar el riesgo de futuros incidentes'),
    dcc.Graph(
        id = 'sample-graph',
        figure = px.line(df[['age_shooter1','count']].iloc[0:42], x='age_shooter1', y='count', title='Edad').update_layout(
            xaxis_title = 'Edad',
            yaxis_title = 'Conteo'
            )
       
        )
    ])


conn.close()

if __name__ == '__main__' :
    app.run_server(port=8085)