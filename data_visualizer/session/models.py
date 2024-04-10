""" This module contains the data models for CommuniData "sessions" app.

    Classes:
        Consultant (models.Model): The data model for consultants.
        BusinessInitiativeProgram (models.Model): The data model for Business Initiative Programs (BIPs)
    
"""

from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.core.validators import RegexValidator


MAX_CHAR_LENGTH = 100
PHONE_REGEX = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)
SPECIALTY_CHOICES = [
    ('1', 'Capital Specialist'),
    ('2', 'Financial Specialist'),
    ('3', 'Licensing Specialist'),
    ('4', 'Cultural Specialist'),
    ('5', 'Technology Specialist'),
    ('6', 'Other')
]
PIN_REGEX = RegexValidator(
    regex=r'^\d{2}-\d{2}-\d{3}-\d{3}-\d{4}$',
    message="PIN must be in the format 00-00-000-000-0000."
)
PROPERTY_CLASS_REGEX = RegexValidator(
    regex=r'^\d{1}-\d{2}$',
    message="Property class must be in the format 0-00."
)


class Consultant(models.Model):
    """Consultant data model.

    Args:
        models (module): The Django models module.
        consultantId (int, optional): The ID of the consultant. Defaults to models.AutoField(primary_key=True).

    Attributes:
        consultant_id (int): The ID of the consultant and Primary Key of the table.
        first_name (str): The first name of the consultant.
        last_name (str): The last name of the consultant.
        slug (str): The slug field for the consultant's URL, auto-generated if not provided.
        email (str): The email address of the consultant.
        phone (str): The phone number of the consultant.
        specialty (str): The specialty of the consultant chosen from the list of specialites.
        bip_id (int): The BIP (Business Initiatives Program) ID and foreign key of the consultant.
        
    """

    consultant_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    last_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    slug = models.SlugField(max_length=MAX_CHAR_LENGTH * 2, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=MAX_CHAR_LENGTH)
    phone = models.CharField(validators=[PHONE_REGEX], max_length=15)
    specialty = models.CharField(choices=SPECIALTY_CHOICES, max_length=2)
    bip_id = models.ForeignKey('BusinessInitiativeProgram', on_delete=models.CASCADE)

    class Meta:
        db_table = 'consultants'
        constraints = [
            CheckConstraint(
                check=Q(specialty__in=[choice[0] for choice in SPECIALTY_CHOICES]),
                name='valid_specialty',
            ),
        ]

    def save(self, *args, **kwargs):
        """ Overriding the save method to auto-generate the slug field if not provided.
        
            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.
                
        """
        if not self.slug:
            self.slug = f"{self.first_name}-{self.last_name}"
        super(Consultant, self).save(*args, **kwargs)
            

class BusinessInitiativeProgram(models.Model):
    """Business Initiative Program (BIP) data model.

    Args:
        models (module): The Django models module.
        bipId (int, optional): The ID of the BIP. Defaults to models.AutoField(primary_key=True).

    Attributes:
        bipId (int): The ID of the BIP and Primary Key of the table.
        name (str): The name of the BIP.
        deliverables (str): The deliverables of the BIP.
        start_date (Date): The start date of the BIP.
        end_date (Date): The end date of the BIP.
        contact (str): The contact person for the BIP.
        
    """

    bip_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    deliverables = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    contact = models.CharField(max_length=MAX_CHAR_LENGTH)

    class Meta:
        db_table = 'bips'
        
        
class Buildings(models.Model):
    """Building data model.

    Args:
        models (module): The Django models module.
        buildingId (int, optional): The ID of the building. Defaults to models.AutoField(primary_key=True).

    Attributes:
        pin: CharField (Personal Identification Number, no dashes)
        address: CharField (Full address)
        address_number: CharField or IntegerField (Address number)
        address_street: CharField (Street name of address)
        zip_code: CharField or IntegerField (ZIP code)
        chicago_owned_property: CharField (Boolean-like, might need clarification)
        property_class: CharField or IntegerField (Class code)
        property_description: TextField (Description of the property)
        bill_2020: DecimalField (Property tax bill amount for 2020)
        bill_2021: DecimalField (Property tax bill amount for 2021)
        assessment_2020: DecimalField (Property tax assessment for 2020)
        assessment_2021: DecimalField (Property tax assessment for 2021)
        units: IntegerField (Number of units)
        area_sq_ft: DecimalField (Area in square feet)
        lot_size_sf: DecimalField (Lot size in square feet)
        property_tax_year: IntegerField (The tax year for the property)
        taxpayer_name: CharField (Name of the taxpayer)
        taxpayer_address: CharField (Address of the taxpayer)
        taxpayer_city_state_zip: CharField (City, state, and ZIP of the taxpayer)
        time_last_checked: DateTimeField (Last time the data was checked)
        
    """

    building_id = models.AutoField(primary_key=True)
    pin = models.CharField(validators=[PIN_REGEX], max_length=20)
    address = models.CharField(max_length=MAX_CHAR_LENGTH)
    address_number = models.IntegerField()
    address_street = models.CharField(max_length=MAX_CHAR_LENGTH)
    zip_code = models.IntegerField()
    chicago_owned_property = models.BooleanField()
    property_class = models.CharField(validators=[PROPERTY_CLASS_REGEX], max_length=5)
    property_description = models.TextField()
    tax_bill_2020 = models.DecimalField(max_digits=10, decimal_places=2)
    tax_bill_2021 = models.DecimalField(max_digits=10, decimal_places=2)
    assessment_2020 = models.DecimalField(max_digits=10, decimal_places=2)
    assessment_2021 = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.IntegerField()
    area_sq_ft = models.DecimalField(max_digits=10, decimal_places=2)
    lot_size_sf = models.DecimalField(max_digits=10, decimal_places=2)
    property_tax_year = models.IntegerField()
    taxpayer_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    taxpayer_address = models.CharField(max_length=MAX_CHAR_LENGTH)
    taxpayer_city_state_zip = models.CharField(max_length=MAX_CHAR_LENGTH)
    time_last_checked = models.DateTimeField()
    

    class Meta:
        db_table = 'buildings'
        constraints = [
            UniqueConstraint(
                fields=['pin', 'address_number'],
                name='unique_building',
            ),
        ]
        