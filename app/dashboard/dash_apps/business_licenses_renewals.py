import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
from sqlalchemy import create_engine
import os
import calendar

# Create a new Dash app
app = DjangoDash('BusinessLicensesRenewals')

# Connect to the database
def get_data():
    db_url = f"postgresql://{os.environ.get('SQL_USER')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}:{os.environ.get('SQL_PORT')}/{os.environ.get('SQL_NAME')}"
    engine = create_engine(db_url)
    query = "SELECT legal_name, doing_business_as_name, application_type, license_description, license_term_start_date, license_term_expiration_date FROM business_licenses_full"
    df = pd.read_sql(query, engine)
    return df

# Get the data
df = get_data()

# Data processing and science - filter and sort for renewals due within 30 days

df['license_term_start_date'] = pd.to_datetime(df['license_term_start_date'], errors='coerce')
df['license_term_expiration_date'] = pd.to_datetime(df['license_term_expiration_date'], errors='coerce')

if df['license_term_start_date'].isnull().any():
    print('There are missing values in the license_term_start_date column')

if df['license_term_expiration_date'].isnull().any():
    print('There are missing values in the license_term_expiration_date column')
    
values_to_drop = ['c_loc', 'c_sba', 'c_expa', 'c_capa']

df = df[~df['application_type'].isin(values_to_drop)]
    
def get_renewals_due(df, days=30):
    today = pd.Timestamp.today().normalize()
    renewals_due = df[(df['license_term_expiration_date'] - today).dt.days <= days]
    
    if renewals_due.empty:
        print(f"No renewals due within {days} days.")
        return df.sort_values('license_term_expiration_date', ascending=False).head(10)
    
    return renewals_due

# App layout and callback

app.layout = html.Div([
    dcc.Slider(
        id='days-slider',
        min=1,
        max=60,
        step=1,
        value=30,
        marks={i: str(i) for i in range(0, 61, 10)},
    ),
    dash_table.DataTable(
        id='renewals-table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        page_size=10,
    ),
])

@app.callback(
    Output('graph', 'figure'),
    Input('year-radio', 'value'),
    Input('threshold-slider', 'value'),
)
def update_table(days):
    return get_renewals_due(df, days)
    

if __name__ == '__main__':
    app.run_server(debug=True)
