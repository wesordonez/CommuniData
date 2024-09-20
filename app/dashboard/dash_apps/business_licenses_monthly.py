import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
from sqlalchemy import create_engine
import os
import calendar

# Create a new Dash app
app = DjangoDash('BusinessLicensesMonthly')

# Connect to the database
def get_data():
    db_url = f"postgresql://{os.environ.get('SQL_USER')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}:{os.environ.get('SQL_PORT')}/{os.environ.get('SQL_NAME')}"
    engine = create_engine(db_url)
    query = "SELECT date_issued, account_number FROM business_licenses_full"
    df = pd.read_sql(query, engine)
    return df

# Get the data
df = get_data()

# Process the data to get get count of unique businesses (account numbers) by month

df['date_issued'] = pd.to_datetime(df['date_issued'], errors='coerce')
if df['date_issued'].isnull().any():
    print('There are missing values in the date_issued column')

def get_businesses_by_month(df, year):
    # Ensure date_issued is parsed as datetime
    if df['date_issued'].dtype != 'datetime64[ns]':
        df['date_issued'] = pd.to_datetime(df['date_issued'], errors='coerce')
    
    # Check for any invalid dates
    if df['date_issued'].isnull().any():
        print("There are invalid dates in the data.")
        
    df['month'] = df['date_issued'].dt.month
    df['year'] = df['date_issued'].dt.year
    
    df_year = df[df['year'] == year]
    
    if df_year.empty:
        print(f"No data available for year {year}.")
        return pd.DataFrame()
    
    df_monthly = df_year.groupby('month')['account_number'].nunique().reset_index(name='count')
    
    df_monthly['month'] = df_monthly['month'].apply(lambda x: calendar.month_abbr[x])
    
    return df_monthly

# Create bar chart for unique business licenses by month

df_businesses_by_month_year = get_businesses_by_month(df, 2021)

fig = px.bar(df_businesses_by_month_year, x='month', y='count',
             labels={'month': 'Month', 'count': 'Number of Licenses'})

app.layout = html.Div([
    dcc.RadioItems(
        id='year-radio',
        options=[
            {'label': '2020', 'value': 2020},
            {'label': '2021', 'value': 2021},
            {'label': '2022', 'value': 2022}
        ],
        value=2021,
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='graph', figure=fig)
])

@app.callback(
    Output('graph', 'figure'),
    Input('year-radio', 'value')
)
def update_graph(selected_year):
    df_businesses_by_month_year = get_businesses_by_month(df, selected_year)
    
    fig = px.bar(df_businesses_by_month_year, x='month', y='count',
                 labels={'month': 'Month', 'count': 'Number of Licenses'})
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
