""" This module contains the data models for CommuniData app.

    Classes:
        Consultant (models.Model): The data model for consultants.
    
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


class Consultant(models.Model):
    """Consultant data model.

    Args:
        models (module): The Django models module.
        consultantId (int, optional): The ID of the consultant. Defaults to models.AutoField(primary_key=True).

    Attributes:
        consultantId (int): The ID of the consultant and Primary Key of the table.
        first_name (str): The first name of the consultant.
        last_name (str): The last name of the consultant.
        slug (str): The slug field for the consultant's URL, auto-generated if not provided.
        email (str): The email address of the consultant.
        phone (str): The phone number of the consultant.
        specialty (str): The specialty of the consultant chosen from the list of specialites.
        bip_id (int): The BIP (Business Initiatives Program) ID and foreign key of the consultant.
        
    """

    consultantId = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    last_name = models.CharField(max_length=MAX_CHAR_LENGTH)
    slug = models.SlugField(max_length=MAX_CHAR_LENGTH * 2, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=MAX_CHAR_LENGTH)
    phone = models.CharField(validators=[PHONE_REGEX], max_length=15)
    specialty = models.CharField(choices=SPECIALTY_CHOICES, max_length=2)
    bip_id = models.IntegerField()

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
            self.slug = f"{self.first_name}-{self.last_name}-{self.bip_id}"
        super(Consultant, self).save(*args, **kwargs)
            
    