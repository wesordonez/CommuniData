import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
from sqlalchemy import create_engine
import os
import calendar
import geopandas as gpd
from shapely.geometry import Point, Polygon
from django.conf import settings
import plotly.graph_objects as go


# Create a new Dash app
app = DjangoDash('BusinessLicensesMap')

# Connect to the database
def get_data():
    db_url = f"postgresql://{os.environ.get('SQL_USER')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}:{os.environ.get('SQL_PORT')}/{os.environ.get('SQL_NAME')}"
    engine = create_engine(db_url)
    query = "SELECT account_number, legal_name, doing_business_as_name, address, license_description, application_type, license_term_start_date, license_term_expiration_date, date_issued, latitude, longitude FROM business_licenses_full"
    df = pd.read_sql(query, engine)
    return df

# Get the data
df = get_data()

print(df.columns)
# Data processing and science - Overlay the data on chicago map

    
# Display the map

def create_map(cluster_enabled='enabled', color='color'):
    
    if color == 'color':
        fig = px.scatter_mapbox(
            df,
            lat='latitude',
            lon='longitude',
            hover_name='legal_name',
            hover_data=['doing_business_as_name', 'address', 'license_description', 'license_term_expiration_date'],
            labels={'doing_business_as_name': 'Doing Business As', 'address': 'Address', 'license_description': 'License Description', 'license_term_expiration_date': 'License Term Expiration Date'},
            mapbox_style='carto-positron',
            height=950,
            zoom=13,
            color='application_type',
        )   
    else:
        fig = px.scatter_mapbox(
            df,
            lat='latitude',
            lon='longitude',
            hover_name='legal_name',
            hover_data=['doing_business_as_name', 'address', 'license_description', 'license_term_expiration_date'],
            labels={'doing_business_as_name': 'Doing Business As', 'address': 'Address', 'license_description': 'License Description', 'license_term_expiration_date': 'License Term Expiration Date'},
            mapbox_style='carto-positron',
            height=950,
            zoom=13,
            # color='application_type',
        )   
    
    if cluster_enabled == 'enabled':
        fig.update_traces(marker=dict(size=15), cluster=dict(enabled=True, step=10, maxzoom=15))

    else:
        fig.update_traces(marker=dict(size=15), cluster=dict(enabled=False, maxzoom=1))

        
    return fig


# heat map requires a "z" value, which is the intensity of the heat. this would be a count of businesses in a given area

# fig = px.density_map(
#     df,
#     lat='latitude',
#     lon='longitude',
#     hover_name='legal_name',
#     hover_data=['doing_business_as_name', 'address', 'license_description', 'application_type', 'license_term_start_date', 'license_term_expiration_date', 'date_issued'],
#     title='Business Licenses in Chicago',
#     labels={'latitude': 'Latitude', 'longitude': 'Longitude'},
#     mapbox_style='carto-positron',
#     height=900,
#     width=900,
#     zoom=13,
# )   

        
# App layout and callback

app.layout = html.Div([
    dcc.RadioItems(
        id='cluster-toggle',
        options=[
            {'label': 'Enable Clustering', 'value': 'enabled'},
            {'label': 'Disable Clustering', 'value': 'disabled'},
        ],
        value='enabled',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.RadioItems(
        id='color-toggle',
        options=[
            {'label': 'Color by Application Type', 'value': 'color'},
            {'label': 'No Color Separation', 'value': 'no_color'},
        ],
        value='scatter',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='map', figure=create_map(cluster_enabled='enabled'))
])

@app.callback(
    Output('map', 'figure'),
    Input('cluster-toggle', 'value'),
    Input('color-toggle', 'value')
)
def update_map(value, color):
    fig = create_map(value, color)

    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)
