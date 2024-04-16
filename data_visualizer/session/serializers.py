"""This module contains the serializers for CommuniData "sessions" app.

    Classes:
        ConsultantSerializer (serializers.ModelSerializer): The serializer for the Consultant data model.
        BusinessInitiativeProgramSerializer (serializers.ModelSerializer): The serializer for the Business Initiative Program data model.
        
"""


from rest_framework import serializers
from .models import Consultant, BusinessInitiativeProgram as Bip

class ConsultantSerializer(serializers.ModelSerializer):
    """Consultant serializer class.
    
    Args:
        serializers (module): The Django REST framework serializers module.
        Consultant (models.Model): The Consultant data model.
        
    """
    
    class Meta:
        model = Consultant
        fields = '__all__'
        
class BipSerializer(serializers.ModelSerializer):
    """Business Initiative Program serializer class.
    
    Args:
        serializers (module): The Django REST framework serializers module.
        Bip (models.Model): The Business Initiative Program data model.
        
    """
    
    class Meta:
        model = Bip
        fields = '__all__'
        