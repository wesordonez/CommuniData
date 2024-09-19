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

# Process the data to get get count of businesses by month only for 2023

df['date_issued'] = pd.to_datetime(df['date_issued'], errors='coerce')
if df['date_issued'].isnull().any():
    print('There are missing values in the date_issued column')

def get_businesses_by_month():
    df['month'] = df['date_issued'].dt.month
    df['year'] = df['date_issued'].dt.year
    df_2023 = df[df['year'] == 2023]
    return df_2023.groupby(['month']).size().reset_index(name='count')

# Create bar chart for business licenses by month

df_businesses_by_month_2023 = get_businesses_by_month()

fig = px.bar(df_businesses_by_month_2023, x='month', y='count',
             title='Business Licenses by Month in 2023',
             labels={'month': 'Month', 'count': 'Number of Licenses'})

app.layout = html.Div([
    html.H1('Business Licenses Dashboard'),
    dcc.Graph(
        id='business-licenses-by-month',
        figure=fig
    )
])

# # Example Viz
# fig = px.bar(df, x='ward', y='license_number', title='Business Licenses by Ward')

# # Define the layout
# app.layout = html.Div(children=[
#     html.H1(children='Business Licenses Dashboard'),
#     dcc.Graph(
#         id='example-graph',
#         figure=px.bar(get_data(), x='license_id', y='license_status')
#     )
# ])
