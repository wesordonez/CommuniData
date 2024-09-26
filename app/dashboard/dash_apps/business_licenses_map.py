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

# Get the Chicago street map data
shapefile_path = os.path.join(settings.MEDIA_ROOT, 'shapefiles', 'geo_export_bdc85215-02b6-4b86-96a5-1ee57873927b.shp')
chicago_street_map = gpd.read_file(shapefile_path)

# Data processing and science - Overlay the data on chicago map


# test to display the map

print(chicago_street_map.crs)

# Ensure the shapefile is using lat/lon projection (EPSG:4326)
if chicago_street_map.crs is None:
    chicago_street_map = chicago_street_map.set_crs('EPSG:4326')
    
    
print(chicago_street_map['geometry'].isnull().sum())

chicago_street_map = chicago_street_map[chicago_street_map['geometry'].notnull()]


# chicago_street_map['coords'] = chicago_street_map['geometry'].apply(lambda x: x.representative_point().coords[:])

chicago_street_map['coords'] = chicago_street_map['geometry'].apply(lambda x: list(x.coords))

# Extract the centroids of polygons for lat/lon values
# chicago_street_map['lon'] = chicago_street_map.geometry.centroid.x
# chicago_street_map['lat'] = chicago_street_map.geometry.centroid.y

# chicago_street_map = chicago_street_map.to_crs('EPSG:4326')


fig = go.Figure()

for coords in chicago_street_map['coords']:
    lons, lats = zip(*coords)
    fig.add_trace(go.Scattermap(
        mode='lines',
        lon=lons,
        lat=lats,
        line=dict(width=2),
        name='Street Line'
    ))



# px.set_mapbox_access_token(open(".mapbox_token").read())
# fig = px.scatter_map(chicago_street_map,
#                      map_style='open-street-map',
#                      title='Business Licenses in Chicago')


        
        
# App layout and callback

app.layout = html.Div([
    dcc.Graph(id='map', figure=fig)
])

# @app.callback(
#     Output('avg-length-table', 'data'),
#     Output('time-unit-output', 'children'),
#     Input('time-unit', 'value'),
# )
# def update_table(value):
#     table_update, time_unit_label = get_table(time_unit=value)
#     return table_update.to_dict('records') , f''
    

if __name__ == '__main__':
    app.run_server(debug=True)
