import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
from sqlalchemy import create_engine
import os
import calendar

# Create a new Dash app
app = DjangoDash('BusinessLicensesDistribution')

# Connect to the database
def get_data():
    if os.environ.get('DJANGO_ENV') == 'development':
        db_url = f"postgresql://{os.environ.get('SQL_USER')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}:{os.environ.get('SQL_PORT')}/{os.environ.get('SQL_NAME')}"
    else:
        db_url = f"postgresql://{os.environ.get('PRD_SQL_USER')}:{os.environ.get('PRD_SQL_PASSWORD')}@{os.environ.get('PRD_SQL_HOST')}:{os.environ.get('PRD_SQL_PORT')}/{os.environ.get('PRD_SQL_NAME')}"
    engine = create_engine(db_url)
    query = "SELECT date_issued, license_description FROM business_licenses_full"
    
    return pd.read_sql(query, engine)

# Get the data
df = get_data()

# Data processing and science - get distribution of business licenses by year

df['date_issued'] = pd.to_datetime(df['date_issued'], errors='coerce')
if df['date_issued'].isnull().any():
    print('There are missing values in the date_issued column')
    
def get_distribution_by_year(df, year, threshold=0.05):
    df['year'] = df['date_issued'].dt.year
    df_year = df[df['year'] == year]

    df_distribution = df_year['license_description'].value_counts(normalize=True).reset_index()
    df_distribution.columns = ['license_description', 'proportion']

    categories_to_group = df_distribution['license_description'][df_distribution['proportion'] < threshold].unique()

    df_year['grouped_category'] = df_year['license_description'].apply(lambda x: 'Other' if x in categories_to_group else x)
    df_distribution = df_year['grouped_category'].value_counts().reset_index()
    df_distribution.columns = ['grouped_category', 'count']

    return df_distribution

df_distribution = get_distribution_by_year(df, 2021)

fig = px.pie(df_distribution, values='count', names='grouped_category',)
fig.update_traces(textposition='outside', textinfo='percent+label')
fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-1,
            xanchor='center',
            x=0.5
    )
    )

# App layout and callback

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
    dcc.Slider(
        id='threshold-slider',
        min=1,
        max=10,
        step=1,
        value=5,
        marks={i: f'{i}%' for i in range(1, 11)}
    ),
    dcc.Graph(id='graph', figure=fig)
])

@app.callback(
    Output('graph', 'figure'),
    Input('year-radio', 'value'),
    Input('threshold-slider', 'value'),
)
def update_graph(selected_year, threshold):
    df_distribution = get_distribution_by_year(df, selected_year, threshold/100)
    
    fig = px.pie(df_distribution, values='count', names='grouped_category',)
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-1,
            xanchor='center',
            x=0.5
    )
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
