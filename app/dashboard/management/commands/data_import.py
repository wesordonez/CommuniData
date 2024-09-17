""" This script will import the data from the business_licenses.csv file into the database. Will not be used during production.
"""

from django.core.management.base import BaseCommand
from dashboard.models import BusinessLicenses
import pandas as pd
import requests
from io import StringIO
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# API URL for fetching the data from Chicago Data Portal
url = "https://data.cityofchicago.org/resource/4mfv-i89s.csv?$query=SELECT%0A%20%20%60id%60%2C%0A%20%20%60license_id%60%2C%0A%20%20%60account_number%60%2C%0A%20%20%60site_number%60%2C%0A%20%20%60legal_name%60%2C%0A%20%20%60doing_business_as_name%60%2C%0A%20%20%60address%60%2C%0A%20%20%60city%60%2C%0A%20%20%60state%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60ward%60%2C%0A%20%20%60precinct%60%2C%0A%20%20%60ward_precinct%60%2C%0A%20%20%60police_district%60%2C%0A%20%20%60license_code%60%2C%0A%20%20%60license_description%60%2C%0A%20%20%60business_activity_id%60%2C%0A%20%20%60business_activity%60%2C%0A%20%20%60license_number%60%2C%0A%20%20%60application_type%60%2C%0A%20%20%60application_created_date%60%2C%0A%20%20%60application_requirements_complete%60%2C%0A%20%20%60payment_date%60%2C%0A%20%20%60conditional_approval%60%2C%0A%20%20%60license_start_date%60%2C%0A%20%20%60expiration_date%60%2C%0A%20%20%60license_approved_for_issuance%60%2C%0A%20%20%60date_issued%60%2C%0A%20%20%60license_status%60%2C%0A%20%20%60license_status_change_date%60%2C%0A%20%20%60ssa%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%0AWHERE%0A%20%20(%60ward%60%20IN%20(%2226%22))%0A%20%20AND%20(%60date_issued%60%0A%20%20%20%20%20%20%20%20%20BETWEEN%20%222024-09-01T04%3A03%3A33%22%20%3A%3A%20floating_timestamp%0A%20%20%20%20%20%20%20%20%20AND%20%222024-09-17T04%3A03%3A33%22%20%3A%3A%20floating_timestamp)"

app_token = "CDP_APP_TOKEN"

headers = {
    "X-App-Token": app_token
}

response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    api_data = StrigIO(response.text)
    df = pd.read_csv(api_data)
else:
    print("Failed to fetch data from the API. Status code: ", response.status_code)

# Path to the csv file

file_path = '../business_licenses_test.csv'


# Read csv file and set encoding to utf-8
def read_csv_auto(file_path):
    return pd.read_csv(file_path, encoding='utf-8')



class Command(BaseCommand):
    help = 'Imports data from business_licenses.csv into the database.'
    
    def handle(self, *args, **options):
        
        # Import and clean the data
        
        # df = read_csv_auto(file_path)
        df.columns = df.columns.str.lower()
        
        for column in df.columns:
            df.rename(columns={column: column.replace(" ", "_")}, inplace=True)
        date_columns = ['application_created_date', 'application_requirements_complete', 'payment_date', 'license_term_start_date', 'license_term_expiration_date', 'license_approved_for_issuance', 'date_issued', 'license_status_change_date']
        for column in date_columns:
            df[column] = pd.to_datetime(df[column], format='%m/%d/%Y', errors='coerce').dt.date
        df = df.where(pd.notnull(df), None)
        
        # Create and persist data in the database
        
        for index, row in df.iterrows():
            try:
                BusinessLicenses.objects.create(
                    business_id=row['id'],
                    license_id=row['license_id'],
                    account_number=row['account_number'],
                    site_number=row['site_number'],
                    legal_name=row['legal_name'],
                    doing_business_as_name=row['doing_business_as_name'],
                    address=row['address'],
                    city=row['city'],
                    state=row['state'],
                    zip_code=row['zip_code'],
                    ward=row['ward'],
                    precinct=row['precinct'],
                    ward_precinct=row['ward_precinct'],
                    police_district=row['police_district'],
                    license_code=row['license_code'],
                    license_description=row['license_description'],
                    business_activity_id=row['business_activity_id'],
                    business_activity=row['business_activity'],
                    license_number=row['license_number'],
                    application_type=row['application_type'],
                    application_created_date=row['application_created_date'],
                    application_requirements_complete=row['application_requirements_complete'],
                    payment_date=row['payment_date'],
                    conditional_approval=row['conditional_approval'],
                    license_term_start_date=row['license_term_start_date'],
                    license_term_expiration_date=row['license_term_expiration_date'],
                    license_approved_for_issuance=row['license_approved_for_issuance'],
                    date_issued=row['date_issued'],
                    license_status=row['license_status'],
                    license_status_change_date=row['license_status_change_date'],
                    ssa=row['ssa'],
                    latitude=row['latitude'],
                    longitude=row['longitude'],
                    location=row['location'],
                )
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                
        # Success message
        
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
    