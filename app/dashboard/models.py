""" This module contains the data models for CommuniData "dashboard" app.

    Classes:
        # Update
    
"""

from django.db import models


class BusinessLicenses(models.Model):
    """ Model for the Business Licenses data.

        
        Fields:
            id: A calculated ID for each record. (Plain Text)
            license_id: An internal database ID for each record. Each license can have multiple records as it goes through renewals and other transactions. (Number)
            account_number: The account number of the business owner, which will stay consistent across that owner's licenses. (Number)
            site_number: An internal database ID indicating the location of this licensed business. (Number)
            legal_name: (Plain Text)
            doing_business_as_name: (Plain Text)
            address: (Plain Text)
            city: (Plain Text)
            state: (Plain Text)
            zip_code: (Plain Text)
            ward: The ward where the business is located. (Number)
            precinct: The precinct within the ward where the business is located. (Number)
            ward_precinct: The ward and precinct where the business is located. (Plain Text)
            police_district: (Number)
            license_code: A code for the type of license. (Number)
            license_description: (Plain Text)
            business_activity_id: A code for the business activity. (Plain Text)
            business_activity: (Plain Text)
            license_number: The license number known to the public and generally used in other data sources that refer to the license. (Number)
            application_type: (Plain Text)
            application_created_date: The date the business license application was created. (Date & Time)
            application_requirements_complete: The date all required application documents were received. (Date & Time)
            payment_date: (Date & Time)
            conditional_approval: This pertains to applications that contain liquor licenses. (Plain Text)
            license_term_start_date: (Date & Time)
            license_term_expiration_date: (Date & Time)
            license_approved_for_issuance: The date the license was ready for issuance. (Date & Time)
            date_issued: (Date & Time)
            license_status: (Plain Text)
            license_status_change_date: (Date & Time)
            ssa: Special Service Areas are local tax districts that fund expanded services and programs. (Plain Text)
            latitude: (Number)
            longitude: (Number)
            location: (Location)
            
    """
    
    id = models.AutoField(primary_key=True)    
    business_id = models.CharField()
    license_id = models.IntegerField()
    account_number = models.IntegerField()
    site_number = models.IntegerField()
    legal_name = models.CharField()
    doing_business_as_name = models.CharField()
    address = models.CharField()
    city = models.CharField()
    state = models.CharField()
    zip_code = models.CharField()
    ward = models.IntegerField()
    precinct = models.IntegerField()
    ward_precinct = models.CharField()
    police_district = models.IntegerField()
    license_code = models.IntegerField()
    license_description = models.CharField()
    business_activity_id = models.CharField()
    business_activity = models.CharField()
    license_number = models.IntegerField()
    application_type = models.CharField()
    application_created_date = models.DateTimeField()
    application_requirements_complete = models.DateTimeField()
    payment_date = models.DateTimeField()
    conditional_approval = models.CharField()
    license_term_start_date = models.DateTimeField()
    license_term_expiration_date = models.DateTimeField()
    license_approved_for_issuance = models.DateTimeField()
    date_issued = models.DateTimeField()
    license_status = models.CharField()
    license_status_change_date = models.DateTimeField()
    ssa = models.CharField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.CharField()
    
    class Meta:
        db_table = 'business_licenses_full'   
        
          