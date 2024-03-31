""" This module contains the data models for CommuniData "home" app.

    Classes:
        Review (models.Model): The data model for reviews.
    
"""

from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


MAX_CHAR_LENGTH = 100
PHONE_REGEX = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class Review(models.Model):
    """Review data model.

    Args:
        models (module): The Django models module.

    Attributes:
        review_id (AutoField): The ID of the review and Primary Key of the table.
        name (CharField): The name of the reviewer.
        organization (CharField): The organization of the reviewer.
        message (TextField): The review message.
        stars (IntegerField): The rating given by the reviewer (1 to 5).

    """
    
    review_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    organization = models.CharField(max_length=MAX_CHAR_LENGTH)
    message = models.TextField()
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
   
    class Meta:
        db_table = 'reviews'
       