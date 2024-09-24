import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
from sqlalchemy import create_engine
import os
import calendar

# Create a new Dash app
app = DjangoDash('BusinessLicensesHistogram')

# Connect to the database
def get_data():
    db_url = f"postgresql://{os.environ.get('SQL_USER')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}:{os.environ.get('SQL_PORT')}/{os.environ.get('SQL_NAME')}"
    engine = create_engine(db_url)
    query = "SELECT account_number, license_term_start_date, license_term_expiration_date, date_issued FROM business_licenses_full"
    df = pd.read_sql(query, engine)
    return df

# Get the data
df = get_data()

# Data processing and science - filter and sort for renewals due within 30 days

df['license_term_start_date'] = pd.to_datetime(df['license_term_start_date'], errors='coerce')
df['license_term_expiration_date'] = pd.to_datetime(df['license_term_expiration_date'], errors='coerce')
df['date_issued'] = pd.to_datetime(df['date_issued'], errors='coerce')

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
    
if df['date_issued'].isnull().sum() < 0.05 * len(df):
    df.dropna(subset=['date_issued'], inplace=True)
else:
    print('There is a large number missing values in the date_issued column:')
    print(df['date_issued'].isnull().sum())
    print(0.05 * len(df))
    
# Step 1: Separate out the unique accounts
def get_histogram():
    account_counts = df['account_number'].value_counts()
    unique_accounts = account_counts[account_counts == 1].index
    df_unique = df[df['account_number'].isin(unique_accounts)]

    today = pd.Timestamp.today().normalize()

    df_unique['active_status'] = df_unique['license_term_expiration_date'].apply(lambda x: 'Active' if x > today else 'Expired')
    df_unique['operation_time'] = (df_unique['license_term_expiration_date'] - df_unique['license_term_start_date']).dt.days

    if (df_unique['operation_time'] < 0).sum() < 0.05 * len(df_unique):
        df_unique = df_unique[df_unique['operation_time'] >= 0]
    else:
        print('There is a large number of negative values in the operation_time column:')
        print((df_unique['operation_time'] < 0).sum())
        print(0.05 * len(df_unique))
        
    return df_unique
    
df_histogram = get_histogram() 

fig = px.histogram(df_histogram, x='operation_time', color='active_status', nbins=20, title='Histogram of Operation Time for Unique Accounts')  
        

    
    
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
    dcc.Graph(id='histogram', figure=fig)
])

# @app.callback(
#     Output('renewals-table', 'data'),
#     Input('days-slider', 'value'),
# )
# def update_table(days):
#     renewals_update = get_renewals_due(df, days)
    
#     if renewals_update.empty:
#         return f"No renewals due within {days} days."
    
#     return renewals_update.to_dict('records')
    

if __name__ == '__main__':
    app.run_server(debug=True)
