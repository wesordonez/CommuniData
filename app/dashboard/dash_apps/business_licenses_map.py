import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd
from sqlalchemy import create_engine
import os
import calendar

# Create a new Dash app
app = DjangoDash('BusinessLicensesMap')

# Connect to the database
def get_data():
    db_url = f"postgresql://{os.environ.get('SQL_USER')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}:{os.environ.get('SQL_PORT')}/{os.environ.get('SQL_NAME')}"
    engine = create_engine(db_url)
    query = "SELECT account_number, license_term_start_date, license_term_expiration_date, date_issued, license_description FROM business_licenses_full"
    df = pd.read_sql(query, engine)
    return df

# Get the data
df = get_data()

# Data processing and science - Overlay the data on chicago map



        
# App layout and callback

app.layout = html.Div([
    # dcc.Dropdown(
    #     ['Days', 'Months', 'Years'],
    #     'Days',
    #     id='time-unit',
    # ),
    # html.Div(id='time-unit-output'),
    # dash_table.DataTable(
    #     id='avg-length-table',
    #     data=df_avg_operation_length.to_dict('records'),
    #     columns=[
    #         {'name': 'License Description', 'id': 'license_description'},
    #         {'name': 'Average Operation Time', 'id': 'avg_operation_time'},
    #     ],
    #     style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
    #     style_cell_conditional=[
    #         {
    #             'if': {'column_id': 'license_description'},
    #             'textAlign': 'left'
    #         }
    #     ],
    # ),
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
