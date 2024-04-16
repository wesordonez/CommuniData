from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Consultant, BusinessInitiativeProgram as Bip
from .serializers import ConsultantSerializer, BipSerializer
from django.core.exceptions import ValidationError
from django.http import Http404

# Removing CSRF token from the form for testing purposes. This needs to be removed later.
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class ConsultantAPIView(APIView):
    """Consultant API view class.
    
    This class is used to define CRUD operations for the Consultant API.
    
    Methods:
        get: Handles GET requests.
        post: Handles POST requests.
        
    """
    
    def get(self, request, consultant_id=None):
        
        consultants = Consultant.objects.all()
        serializer = ConsultantSerializer(consultants, many=True)
        return Response(serializer.data)
    
    def get_consultant_by_id(self, consultant_id):
        
        try:
            consultant_db = Consultant.objects.get(consultant_id=consultant_id)
            return consultant_db
        except Consultant.DoesNotExist:
            raise Http404('Consultant does not exist.')
    
        
    def post(self, request):
        
        serializer = ConsultantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, consultant_id):
        
        consultant = self.get_consultant_by_id(consultant_id)
        serializer = ConsultantSerializer(consultant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@method_decorator(csrf_exempt, name='dispatch')
class BipAPIView(APIView):
    """Bip API view class.
    
    This class is used to define CRUD operations for the Bip API.
    
    Methods:
        get: Handles GET requests.
        post: Handles POST requests.
        
    """
    
    def get(self, request):
        
        bip = Bip.objects.all()
        serializer = BipSerializer(bip, many=True)
        return Response(serializer.data)
    
        
    def post(self, request):
        
        serializer = BipSerializer(data=request.data)
        if serializer.is_valid():
            try:
                instance = Bip(**serializer.validated_data)
                instance.full_clean()
                instance.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    