from django.db import models
from django.core.validators import RegexValidator


MAX_CHAR_LENGTH = 100
PHONE_REGEX = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

    
class Consultant(models.Model):
    """Consultant data model.

    Args:
        models (_type_): _description_
        consultantId (int, optional): _description_. Defaults to models.AutoField(primary_key=True).
    """
    SPECIALTY_CHOICES = [
        ('1', 'Capital Specialist'),
        ('2', 'Financial Specialist'),
        ('3', 'Licensing Specialist'),
        ('4', 'Cultural Specialist'),
        ('5', 'Technology Specialist'),
        ('6', 'Other')
    ]
    
    consultantId = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    last_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    email = models.EmailField()
    phone = models.CharField(validators=[PHONE_REGEX], max_length=15)
    specialty = models.CharField(choices=SPECIALTY_CHOICES, max_length=100)
    bip_id = models.IntegerField()
    
    
    class Meta:
        db_table = 'consultants'
        
    