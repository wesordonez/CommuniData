import dash
from dash import dcc, html
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
from sqlalchemy import create_engine
import os


# Create a new Dash app
app = DjangoDash('BusinessDashboard')

# Connect to the database
def get_data():
    db_url = f"postgresql://{os.environ.get('SQL_USER')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}:{os.environ.get('SQL_PORT')}/{os.environ.get('SQL_NAME')}"
    engine = create_engine(db_url)
    query = "SELECT * FROM business_licenses_full"
    df = pd.read_sql(query, engine)
    return df

# Get the data
df = get_data()

# Example Viz
fig = px.bar(df, x='ward', y='license_number', title='Business Licenses by Ward')

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Business Licenses Dashboard'),
    dcc.Graph(
        id='example-graph',
        figure=px.bar(get_data(), x='license_id', y='license_status')
    )
])
