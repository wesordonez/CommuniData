""" This module contains the data models for CommuniData "sessions" app.

    Classes:
        Consultant (models.Model): The data model for consultants.
        BusinessInitiativeProgram (models.Model): The data model for Business Initiative Programs (BIPs)
    
"""

from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


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
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('N', 'Prefer not to say')
]
INDUSTRY_CHOICES = [
    ('1', 'Agriculture, Forestry, Fishing and Hunting'),
    ('2', 'Mining, Quarrying, and Oil and Gas Extraction'),
    ('3', 'Utilities'),
    ('4', 'Construction'),
    ('5', 'Manufacturing'),
    ('6', 'Wholesale Trade'),
    ('7', 'Retail Trade'),
    ('8', 'Transportation and Warehousing'),
    ('9', 'Information'),
    ('10', 'Finance and Insurance'),
    ('11', 'Real Estate and Rental and Leasing'),
    ('12', 'Professional, Scientific, and Technical Services'),
    ('13', 'Management of Companies and Enterprises'),
    ('14', 'Administrative and Support and Waste Management and Remediation Services'),
    ('15', 'Educational Services'),
    ('16', 'Health Care and Social Assistance'),
    ('17', 'Arts, Entertainment, and Recreation'),
    ('18', 'Accommodation and Food Services'),
    ('19', 'Other Services (except Public Administration)'),
    ('20', 'Public Administration')
]
LEGAL_STRUCTURE_CHOICES = [
    ('1', 'Sole Proprietorship'),
    ('2', 'Partnership'),
    ('3', 'Corporation'),
    ('4', 'S Corporation'),
    ('5', 'Limited Liability Company (LLC)'),
    ('6', 'Nonprofit Corporation'),
    ('7', 'Cooperative'),
    ('8', 'Other')
]
EIN_REGEX = RegexValidator(
    regex=r'^\d{2}-\d{7}$',
    message="EIN must be in the format 00-0000000."
)
STATUS_CHOICES = ['Active', 'Inactive', 'Closed']


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
        
    def clean(self):
        """ Overriding the clean method to ensure the start date is before the end date.
        
        """
        super().clean()
        if self.start_date > timezone.now().date():
            raise ValidationError("The start date must be before today.")
        
        if self.start_date > self.end_date:
            raise ValidationError("The start date must be before the end date.")
        
        
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
        
        
class Contacts(models.Model):
    """Contact data model.
    
    Args:
        models (module): The Django models module.
        contactId (int, optional): The ID of the contact. Defaults to models.AutoField(primary_key=True).

    Attributes:
        contactId (int): The ID of the contact and Primary Key of the table.
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (str): The email address of the contact.
        phone (str): The phone number of the contact.
        business_id (int): Foreign Key to the company the contact is associated with.
        business_role (str): The role of the contact in the business.
        alt_phone (str): An alternate phone number for the contact.
        address (str): The mailing address of the contact.
        date_of_birth (Date): The date of birth of the contact.
        gender (str): The gender of the contact.
        ethnicity (str): The ethnicity of the contact.
        nationality (str): The nationality of the contact.
        language (str): The language spoken by the contact.
        registration_date (Date): The date the contact was registered.
        notes (str): Any notes about the contact.
        created_at (DateTime): The date and time the contact was created.
        updated_at (DateTime): The date and time the contact was last updated.
        
    """
    
    contact_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    last_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    email = models.EmailField(max_length=MAX_CHAR_LENGTH)
    phone = models.CharField(validators=[PHONE_REGEX], max_length=15)
    business_id = models.ForeignKey('Business', on_delete=models.CASCADE)
    business_role = models.CharField(max_length=MAX_CHAR_LENGTH)
    alt_phone = models.CharField(validators=[PHONE_REGEX], max_length=15)
    address = models.CharField(max_length=MAX_CHAR_LENGTH)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=MAX_CHAR_LENGTH)
    ethnicity = models.CharField(max_length=MAX_CHAR_LENGTH)
    nationality = models.CharField(max_length=MAX_CHAR_LENGTH)
    language = models.CharField(max_length=MAX_CHAR_LENGTH)
    registration_date = models.DateField()
    notes = models.TextField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contacts'
        constraints = [
            CheckConstraint(
                check=Q(date_of_birth__lte=timezone.now().date()),
                name='valid_date_of_birth',
            ),
            CheckConstraint(
                check=Q(gender__in=[choice[0] for choice in GENDER_CHOICES]),
                name='valid_gender_choice',
            ),
            CheckConstraint(
                check=Q(registration_date__lte=timezone.now().date()),
                name='valid_registration_date',
            ),
        ]
        
        
class Business(models.Model):
    """Business data model.

    Args:
        models (module): The Django models module.
        businessId (int, optional): The ID of the business. Defaults to models.AutoField(primary_key=True).
        
    Attributes:
        business_id (int): The ID of the business and Primary Key of the table.
        name (str): The name of the business.
        dba (str): The "doing business as" name of the business.
        business_description (str): The description of the business.
        address (str): The address of the business.
        phone (str): The phone number of the business.
        email (str): The email address of the business.
        website (str): The website of the business.
        industry (str): The industry the business is in.
        naics_code (str): The NAICS code of the business.
        date_established (Date): The date the business was established.
        legal_structure (str): The legal structure of the business.
        ein (str): The Employer Identification Number of the business.
        licenses (str): The licenses the business has.
        contact_id (int): Foreign Key of the contact person for the business.
        num_employees (int): The number of employees at the business.
        status (str): The status of the business.
        notes (str): Any notes about the business.
        created_at (DateTime): The date and time the business was created.
        updated_at (DateTime): The date and time the business was last updated.
    
    """
    
    business_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    dba = models.CharField(max_length=MAX_CHAR_LENGTH)
    description = models.TextField(default='')
    address = models.CharField(max_length=MAX_CHAR_LENGTH)
    phone = models.CharField(validators=[PHONE_REGEX], max_length=15)
    email = models.EmailField(max_length=MAX_CHAR_LENGTH)
    website = models.URLField
    industry = models.CharField(max_length=MAX_CHAR_LENGTH)
    naics_code = models.CharField(max_length=6)
    date_established = models.DateField(null=True, blank=True)
    legal_structure = models.CharField(max_length=MAX_CHAR_LENGTH)
    ein = models.CharField(validators=[EIN_REGEX], max_length=9)
    licenses = models.CharField()
    contact_id = models.ForeignKey('Contacts', on_delete=models.CASCADE)
    num_employees = models.IntegerField
    status = models.CharField(max_length=MAX_CHAR_LENGTH)
    notes = models.TextField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'businesses'
        constraints = [
            CheckConstraint(
                check=Q(industry__in=[choice[0] for choice in INDUSTRY_CHOICES]),
                name='valid_industry',
            ),
            CheckConstraint(
                check=Q(date_established__lte=timezone.now().date()),
                name='valid_date_established',
            ),
            CheckConstraint(
                check=Q(legal_structure__in=[choice[0] for choice in LEGAL_STRUCTURE_CHOICES]),
                name='valid_legal_structure',
            ),
            CheckConstraint(
                check=Q(status__in=STATUS_CHOICES),
                name='valid_status',
            ),
        ]
            
        
        
class Clients(models.Model):
    """Client data model.

    Args:
        models (module): The Django models module.
        clientId (int, optional): The ID of the client. Defaults to models.AutoField(primary_key=True).
        
    Attributes:
        client_id (int): The ID of the client and Primary Key of the table.
        business_id (int): Foreign Key to the business the client is associated with.
        contact_id (int): Foreign Key to the contact person for the client.
        consultant_id (int): Foreign Key to the consultant the client is associated with.
        status (str): The status of the client.
        notes (str): Any notes about the client.
        
    """
    
    client_id = models.AutoField(primary_key=True)
    business_id = models.ForeignKey('Business', on_delete=models.CASCADE)
    contact_id = models.ForeignKey('Contacts', on_delete=models.CASCADE)
    consultant_id = models.ForeignKey('Consultant', on_delete=models.CASCADE)
    status = models.CharField(max_length=MAX_CHAR_LENGTH)
    notes = models.TextField
    
    class Meta:
        db_table = 'clients'
        constraints = [
            UniqueConstraint(
                fields=['business_id', 'contact_id'],
                name='unique_client',
            ),
        ]
        
        
class Sessions(models.Model):
    """Session data model.

    Args:
        models (module): The Django models module.
        sessionId (int, optional): The ID of the session. Defaults to models.AutoField(primary_key=True).
        
    Attributes:
        session_id (int): The ID of the session and Primary Key of the table.
        client_id (int): Foreign Key to the client the session is associated with.
        consultant_id (int): Foreign Key to the consultant the session is associated with.
        date (Date): The date of the session.
        duration (Time): The duration of the session (HH:MM).
        notes (str): Any notes about the session.
        status (str): The status of the session.
        follow_up (date): The follow-up date of the session.
        created_at (DateTime): The date and time the session was created.
        updated_at (DateTime): The date and time the session was last updated.        
        
    """
    
    session_id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey('Clients', on_delete=models.CASCADE)
    consultant_id = models.ForeignKey('Consultant', on_delete=models.CASCADE)
    date = models.DateField
    duration = models.TimeField
    notes = models.TextField
    status = models.CharField(max_length=MAX_CHAR_LENGTH)
    follow_up = models.DateField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'advising_sessions'
    