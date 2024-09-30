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

# Data processing and science - Overlay the data on chicago map

df['date_issued'] = pd.to_datetime(df['date_issued'], errors='coerce')
if df['date_issued'].isnull().any():
    print('There are missing values in the date_issued column')
df['license_term_start_date'] = pd.to_datetime(df['license_term_start_date'], errors='coerce')
if df['license_term_start_date'].isnull().any():
    print('There are missing values in the license_term_start_date column')
df['license_term_expiration_date'] = pd.to_datetime(df['license_term_expiration_date'], errors='coerce')
if df['license_term_expiration_date'].isnull().any():
    print('There are missing values in the license_term_expiration_date column')
    
def get_distribution(df, threshold=0.03):

    df_distribution = df['license_description'].value_counts(normalize=True).reset_index()
    df_distribution.columns = ['license_description', 'proportion']

    categories_to_group = df_distribution['license_description'][df_distribution['proportion'] < threshold].unique()

    df['grouped_category'] = df['license_description'].apply(lambda x: 'Other' if x in categories_to_group else x)

    return df

df = get_distribution(df)
    
# Display the map

def create_map(df, cluster_enabled='enabled', color='color'):
    
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
            color='grouped_category',
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

fig = create_map(df)
        
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
    dcc.Slider(
        id='threshold-slider',
        min=1,
        max=10,
        step=1,
        value=5,
        marks={i: f'{i}%' for i in range(1, 11)}
    ),
    dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=df['date_issued'].min(),
        max_date_allowed=df['date_issued'].max(),
        end_date=df['date_issued'].max(),
        display_format='YYYY-MM-DD',
    ),
    html.Div(id='output-container-date-picker-range'),
    dcc.Graph(id='map', figure=fig)
])

@app.callback(
    Output('map', 'figure'),
    # Output('output-container-date-picker-range', 'children'),
    Input('cluster-toggle', 'value'),
    Input('color-toggle', 'value'),
    Input('threshold-slider', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
)

def update_map(value, color, threshold, start_date, end_date):
    if start_date is None or end_date is None:
        return dash.no_update
    
    filtered_df = df[(df['license_term_start_date'] >= start_date) & (df['license_term_start_date'] <= end_date)]
    
    updated_df = get_distribution(filtered_df, threshold/100)

    updated_fig = create_map(updated_df,value, color)

    return updated_fig
    

if __name__ == '__main__':
    app.run_server(debug=True)
