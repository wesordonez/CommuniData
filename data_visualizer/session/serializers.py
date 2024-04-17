"""This module contains the serializers for CommuniData "sessions" app.

    Classes:
        ConsultantSerializer (serializers.ModelSerializer): The serializer for the Consultant data model.
        BusinessInitiativeProgramSerializer (serializers.ModelSerializer): The serializer for the Business Initiative Program data model.
        
"""


from rest_framework import serializers
from .models import Consultant, BusinessInitiativeProgram as Bip, Buildings, Contacts, Business, Clients

class ConsultantSerializer(serializers.ModelSerializer):
    """Consultant serializer class.
    
    Args:
        serializers (module): The Django REST framework serializers module.
        Consultant (models.Model): The Consultant data model.
        
    """
    
    class Meta:
        model = Consultant
        fields = '__all__'
        
    def update(self, instance, validated_data):
        """Updates a Consultant instance.
        
        Args:
            instance (Consultant): The Consultant instance to update.
            validated_data (dict): The validated data to update the instance with.
            
        Returns:
            instance (Consultant): The updated Consultant instance.
            
        """
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.specialty = validated_data.get('specialty', instance.specialty)
        instance.bip_id = validated_data.get('bip_id', instance.bip_id)
        instance.save()
        return instance
    
        
class BipSerializer(serializers.ModelSerializer):
    """Business Initiative Program serializer class.
    
    Args:
        serializers (module): The Django REST framework serializers module.
        Bip (models.Model): The Business Initiative Program data model.
        
    """
    
    class Meta:
        model = Bip
        fields = '__all__'
        
    def update(self, instance, validated_data):
        """Updates a Business Initiative Program instance.
        
        Args:
            instance (Bip): The Business Initiative Program instance to update.
            validated_data (dict): The validated data to update the instance with.
            
        Returns:
            instance (Bip): The updated Business Initiative Program instance.
            
        """
        
        instance.name = validated_data.get('name', instance.name)
        instance.deliverables = validated_data.get('deliverables', instance.deliverables)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.save()
        return instance
        
class BuildingsSerializer(serializers.ModelSerializer):
    """Building serializer class.
    

    Args:
        serializers (_type_): _description_
        
    """
    
    class Meta:
        model = Buildings
        fields = '__all__'
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    
class ContactsSerializer(serializers.ModelSerializer):
    """Contact serializer class.
    
    Args:
        serializers (_type_): _description_
        
    """
    
    class Meta:
        model = Contacts
        fields = '__all__'
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    
class BusinessSerializer(serializers.ModelSerializer):
    """Business serializer class.
    
    Args:
        serializers (_type_): _description_
        
    """
    
    class Meta:
        model = Business
        fields = '__all__'
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    
class ClientsSerializer(serializers.ModelSerializer):
    """Client serializer class.
    
    Args:
        serializers (_type_): _description_
        
    """
    
    class Meta:
        model = Clients
        fields = '__all__'
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    