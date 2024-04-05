"""This module contains the serializers for CommuniData "sessions" app.

    Classes:
        ConsultantSerializer (serializers.ModelSerializer): The serializer for the Consultant data model.
        BusinessInitiativeProgramSerializer (serializers.ModelSerializer): The serializer for the Business Initiative Program data model.
        
"""


from rest_framework import serializers
from .models import Consultant

class ConsultantSerializer(serializers.ModelSerializer):
    """Consultant serializer class.
    
    Args:
        serializers (module): The Django REST framework serializers module.
        Consultant (models.Model): The Consultant data model.
        
    """
    
    class Meta:
        model = Consultant
        fields = '__all__'
        