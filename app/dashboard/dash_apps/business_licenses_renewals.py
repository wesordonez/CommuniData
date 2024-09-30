import dash
from dash import dcc, html, Input, Output, callback, dash_table
from django_plotly_dash import DjangoDash
import pandas as pd
from sqlalchemy import create_engine
import os

# Create a new Dash app
app = DjangoDash('BusinessLicensesRenewals')

# Connect to the database
def get_data():
    if os.environ.get('DJANGO_ENV') == 'development':
        db_url = f"postgresql://{os.environ.get('SQL_USER')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}:{os.environ.get('SQL_PORT')}/{os.environ.get('SQL_NAME')}"
    else:
        db_url = f"postgresql://{os.environ.get('PRD_SQL_USER')}:{os.environ.get('PRD_SQL_PASSWORD')}@{os.environ.get('PRD_SQL_HOST')}:{os.environ.get('PRD_SQL_PORT')}/{os.environ.get('PRD_SQL_NAME')}"
    engine = create_engine(db_url)
    query = "SELECT legal_name, doing_business_as_name, application_type, license_description, license_term_start_date, license_term_expiration_date FROM business_licenses_full"
    
    return pd.read_sql(query, engine)

# Get the data
df = get_data()

# Data processing and science - filter and sort for renewals due within 30 days

df['license_term_start_date'] = pd.to_datetime(df['license_term_start_date'], errors='coerce')
df['license_term_expiration_date'] = pd.to_datetime(df['license_term_expiration_date'], errors='coerce')

if df['license_term_start_date'].isnull().sum() < 0.05 * len(df):
    df.dropna(subset=['license_term_start_date'], inplace=True)
else:
    print('There is a large number of missing values in the license_term_start_date column:')
    print(df['license_term_start_date'].isnull().sum())
    print(0.05 * len(df))


if df['license_term_expiration_date'].isnull().sum() < 0.05 * len(df):
    df.dropna(subset=['license_term_expiration_date'], inplace=True)
else:
    print('There is a large number missing values in the license_term_expiration_date column:')
    print(df['license_term_expiration_date'].isnull().sum())
    print(0.05 * len(df))
    
values_to_drop = ['c_loc', 'c_sba', 'c_expa', 'c_capa']

df = df[~df['application_type'].isin(values_to_drop)]
    
def get_renewals_due(df, days=30):
    today = pd.Timestamp.today().normalize()
    
    df['days_until_expiration'] = (df['license_term_expiration_date'] - today).dt.days
    
    renewals_due = df[(df['days_until_expiration'] >= 0) & (df['days_until_expiration'] <= days)]
        
    if renewals_due.empty:
        print(f"No renewals due within {days} days.")
        return df.sort_values('license_term_expiration_date', ascending=False).head(0)
    
    renewals_due = renewals_due.sort_values('days_until_expiration', ascending=False)
    renewals_due['license_term_start_date'] = renewals_due['license_term_start_date'].dt.strftime('%Y-%m-%d')
    renewals_due['license_term_expiration_date'] = renewals_due['license_term_expiration_date'].dt.strftime('%Y-%m-%d')
    
    return renewals_due

renewals_due = get_renewals_due(df)

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
    html.Div(id='renewals-table-message', style={'color': 'red'}),
    dash_table.DataTable(
        id='renewals-table',
        data=renewals_due.to_dict('records'),
        columns=[
            {'name': 'Legal Name', 'id': 'legal_name'},
            {'name': 'Doing Business As Name', 'id': 'doing_business_as_name'},
            {'name': 'Application Type', 'id': 'application_type'},
            {'name': 'License Description', 'id': 'license_description'},
            {'name': 'License Term Start Date', 'id': 'license_term_start_date'},
            {'name': 'License Term Expiration Date', 'id': 'license_term_expiration_date'},
            {'name': 'Days Until Expiration', 'id': 'days_until_expiration'},
        ],
        page_size=11,
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
    ),
])

@app.callback(
    Output('renewals-table', 'data'),
    Input('days-slider', 'value'),
)
def update_table(days):
    renewals_update = get_renewals_due(df, days)
    
    if renewals_update.empty:
        return f"No renewals due within {days} days."
    
    return renewals_update.to_dict('records')
    

if __name__ == '__main__':
    app.run_server(debug=True)
