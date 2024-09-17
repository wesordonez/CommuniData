import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
import psycopg2
import os


# Create a new Dash app
app = DjangoDash('BusinessDashboard')

# Connect to the database
def get_data():
    connection = psycopg2.connect(user = os.environ.get('SQL_USER'),
                                    password = os.environ.get('SQL_PASSWORD'),
                                    host = os.environ.get('SQL_HOST'),
                                    port = os.environ.get('SQL_PORT'),
                                    database = os.environ.get('SQL_NAME'))
    query = "SELECT * FROM business_licenses_full"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# Get the data
df = get_data()

# Example Viz
fig = px.bar(df, x='ward', y='license_number', title='Business Licenses by Ward')

# Define the layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])
