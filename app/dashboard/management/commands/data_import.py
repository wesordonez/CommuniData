""" This script will import the data from the business_licenses.csv file into the database. Will not be used during production.
"""

from django.core.management.base import BaseCommand
from dashboard.models import BusinessLicenses
import pandas as pd


file_path = '../business_licenses_26th_august_test.csv'


class Command(BaseCommand):
    help = 'Imports data from business_licenses.csv into the database.'
    
    def handle(self, *args, **options):
        
        # Import and clean the data
        
        df = pd.read_csv(file_path, low_memory=False)
        df.columns = df.columns.str.lower()
                
        for column in df.columns:
            df.rename(columns={column: column.replace(" ", "_")}, inplace=True)
        date_columns = ['application_created_date', 'application_requirements_complete', 'payment_date', 'license_term_start_date', 'license_term_expiration_date', 'license_approved_for_issuance', 'date_issued', 'license_status_change_date']
        for column in date_columns:
            df[column] = pd.to_datetime(df[column], format='%m/%d/%Y', errors='coerce').dt.date
        df = df.where(pd.notnull(df), None)
        
        #debugging
        # print(df.head())
        
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
    