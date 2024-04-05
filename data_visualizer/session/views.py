from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Consultant
from .serializers import ConsultantSerializer

# Removing CSRF token from the form for testing purposes. This needs to be removed later.
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class ConsultantAPI(APIView):
    """Consultant API view class.
    
    Args:
        views (module): The Django REST framework views module.
        APIView (class): The Django REST framework API view class.
        Response (class): The Django REST framework response class.
        status (module): The Django REST framework status module.
        Consultant (models.Model): The Consultant data model.
        ConsultantSerializer (serializers.ModelSerializer): The Consultant serializer class.
        
    """
    
    def get(self, request):
        """Handles GET requests.
        
        Args:
            request (Request): The request object.
            
        Returns:
            Response: The response object.
            
        """
        
        consultants = Consultant.objects.all()
        serializer = ConsultantSerializer(consultants, many=True)
        return Response(serializer.data)
    
        
    def post(self, request):
        """Handles POST requests.
        
        Args:
            request (Request): The request object.
            
        Returns:
            Response: The response object.
            
        """
        
        serializer = ConsultantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    