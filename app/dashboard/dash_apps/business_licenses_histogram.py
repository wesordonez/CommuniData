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
    if os.environ.get('DJANGO_ENV') == 'development':
        db_url = f"postgresql://{os.environ.get('SQL_USER')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}:{os.environ.get('SQL_PORT')}/{os.environ.get('SQL_NAME')}"
    else:
        db_url = f"postgresql://{os.environ.get('PRD_SQL_USER')}:{os.environ.get('PRD_SQL_PASSWORD')}@{os.environ.get('PRD_SQL_HOST')}:{os.environ.get('PRD_SQL_PORT')}/{os.environ.get('PRD_SQL_NAME')}"
    engine = create_engine(db_url)
    query = "SELECT account_number, license_term_start_date, license_term_expiration_date, date_issued FROM business_licenses_full"
    
    return pd.read_sql(query, engine)

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
    
def get_histogram(time_unit='Days'):
    
    # Step 1: Separate out the unique accounts
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
        
    # Step 2: Separate out the duplicated account numbers
    duplicated_accounts = account_counts[account_counts > 1].index
    df_duplicated = df[df['account_number'].isin(duplicated_accounts)]
    
    df_operation_time = df_duplicated.groupby('account_number').agg(
        earliest_start_date=('license_term_start_date', 'min'),
        latest_end_date=('license_term_expiration_date', 'max')
    ).reset_index()
    df_operation_time['operation_time'] = (df_operation_time['latest_end_date'] - df_operation_time['earliest_start_date']).dt.days
    
    df_non_duplicated = df_duplicated.drop_duplicates(subset='account_number', keep='first').copy()
    df_merged_non_duplicated = pd.merge(
        df_non_duplicated,
        df_operation_time[['account_number', 'operation_time', 'earliest_start_date', 'latest_end_date']],
        on='account_number',
        how='left'
    )
    df_merged_non_duplicated['license_term_start_date'] = df_merged_non_duplicated['earliest_start_date']
    df_merged_non_duplicated['license_term_expiration_date'] = df_merged_non_duplicated['latest_end_date']
    
    if (df_merged_non_duplicated['operation_time'] < 0).sum() < 0.05 * len(df_merged_non_duplicated):
        df_merged_non_duplicated = df_merged_non_duplicated[df_merged_non_duplicated['operation_time'] >= 0]
    else:
        print('There is a large number of negative values in the operation_time column:')
        print((df_merged_non_duplicated['operation_time'] < 0).sum())
        print(0.05 * len(df_merged_non_duplicated))
    
    df_merged_non_duplicated['active_status'] = df_merged_non_duplicated['license_term_expiration_date'].apply(lambda x: 'Active' if x > today else 'Expired')
    
    df_merged_non_duplicated.drop(columns=['earliest_start_date', 'latest_end_date'], inplace=True)
    
    # Step 3: Concatenate the unique and non-duplicated dataframes
    common_columns = df_unique.columns.intersection(df_merged_non_duplicated.columns)
    df_histogram_merged = pd.concat([df_unique[common_columns], df_merged_non_duplicated[common_columns]])
    
    df_histogram_merged['operation_time_months'] = df_histogram_merged['operation_time'] / 30.44
    df_histogram_merged['operation_time_years'] = df_histogram_merged['operation_time'] / 365.25
    
    if time_unit == 'Months':
        df_histogram_merged['operation_time'] = df_histogram_merged['operation_time_months']
        time_unit_label = 'Months'
    elif time_unit == 'Years':
        df_histogram_merged['operation_time'] = df_histogram_merged['operation_time_years']
        time_unit_label = 'Years'
    else:
        time_unit_label = 'Days'
    
    return df_histogram_merged, time_unit_label
    
df_histogram, time_unit_label = get_histogram(time_unit='Days') 

def plot_histogram(df_histogram, time_unit_label):
    fig = px.histogram(df_histogram, x='operation_time', color='active_status', nbins=30)
    fig.update_layout(
        xaxis_title=f'Operation Time ({time_unit_label})',
        yaxis_title='Count',
        legend_title='License Status',
        bargap=0.1
    )  
    return fig

fig = plot_histogram(df_histogram, time_unit_label)
        
# App layout and callback

app.layout = html.Div([
    dcc.Dropdown(
        ['Days', 'Months', 'Years'],
        'Days',
        id='time-unit',
    ),
    html.Div(id='time-unit-output'),
    dcc.Graph(id='histogram', figure=fig)
])

@app.callback(
    Output('histogram', 'figure'),
    Output('time-unit-output', 'children'),
    Input('time-unit', 'value'),
)
def update_histogram(value):
    histogram_update, time_unit_label = get_histogram(time_unit=value)
    fig = plot_histogram(histogram_update, time_unit_label)
    return fig, f''
    

if __name__ == '__main__':
    app.run_server(debug=True)
