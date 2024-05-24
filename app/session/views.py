from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Consultant, BusinessInitiativeProgram as Bip, Buildings, Contacts, Business, Clients, Sessions
from .serializers import ConsultantSerializer, BipSerializer, BuildingsSerializer, ContactsSerializer, BusinessSerializer, ClientsSerializer, SessionsSerializer
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
        put: Handles PUT requests.
        
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
        put: Handles PUT requests.
        
    """
    
    def get(self, request):
        
        bip = Bip.objects.all()
        serializer = BipSerializer(bip, many=True)
        return Response(serializer.data)
    
    def get_bip_by_id(self, bip_id):
            
        try:
            bip_db = Bip.objects.get(bip_id=bip_id)
            return bip_db
        except Bip.DoesNotExist:
            raise Http404('Bip does not exist.')
    
        
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
    
    def put(self, request, bip_id):
        
        bip = self.get_bip_by_id(bip_id)
        serializer = BipSerializer(bip, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name='dispatch')
class BuildingsAPIView(APIView):
    """Building API view class.
    
    This class is used to define CRUD operations for the Building API.

    Methods:
        get: Handles GET requests.
        put: Handles PUT requests.
        
    """
    
    def get(self, request):
        
        buildings = Buildings.objects.all()
        serializer = BuildingsSerializer(buildings, many=True)
        return Response(serializer.data)
    
    
@method_decorator(csrf_exempt, name='dispatch')
class ContactsAPIView(APIView):
    """Contact API view class.
    
    This class is used to define CRUD operations for the Contact API.

    Methods:
        get: Handles GET requests.
        post: Handles POST requests.
        put: Handles PUT requests.
        
    """
    
    def get(self, request):
        
        contacts = Contacts.objects.all()
        serializer = ContactsSerializer(contacts, many=True)
        return Response(serializer.data)
    
    def get_contact_by_id(self, contact_id):
        
        try:
            contact_db = Contacts.objects.get(contact_id=contact_id)
            return contact_db
        except Contacts.DoesNotExist:
            raise Http404('Contact does not exist.')
        
    def post(self, request):
            
        serializer = ContactsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, contact_id):
        
        contact = self.get_contact_by_id(contact_id)
        serializer = ContactsSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@method_decorator(csrf_exempt, name='dispatch')
class BusinessAPIView(APIView):
    """Business API view class.
    
    This class is used to define CRUD operations for the Business API.

    Methods:
        get: Handles GET requests.
        post: Handles POST requests.
        put: Handles PUT requests.
        
    """
    
    def get(self, request):
        
        business = Business.objects.all()
        serializer = BusinessSerializer(business, many=True)
        return Response(serializer.data)
    
    def get_business_by_id(self, business_id):
        
        try:
            business_db = Business.objects.get(business_id=business_id)
            return business_db
        except Business.DoesNotExist:
            raise Http404('Business does not exist.')
    
    def post(self, request):
        
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, business_id):
        
        business = self.get_business_by_id(business_id)
        serializer = BusinessSerializer(business, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@method_decorator(csrf_exempt, name='dispatch')
class ClientsAPIView(APIView):
    """Clients API view class.
    
    This class is used to define CRUD operations for the Clients API.

    Methods:
        get: Handles GET requests.
        post: Handles POST requests.
        put: Handles PUT requests.
        
    """
    
    def get(self, request):
        
        clients = Clients.objects.all()
        serializer = ClientsSerializer(clients, many=True)
        return Response(serializer.data)
    
    def get_client_by_id(self, client_id):
        
        try:
            client_db = Clients.objects.get(client_id=client_id)
            return client_db
        except Clients.DoesNotExist:
            raise Http404('Client does not exist.')
    
    def post(self, request):
        
        serializer = ClientsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, client_id):
        
        client = self.get_client_by_id(client_id)
        serializer = ClientsSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class SessionAPIView(APIView):
    """Session API view class.
    
    This class is used to define CRUD operations for the Session API.

    Methods:
        get: Handles GET requests.
        post: Handles POST requests.
        put: Handles PUT requests.
        
    """
    
    def get(self, request):
        
        sessions = Sessions.objects.all()
        serializer = SessionsSerializer(sessions, many=True)
        return Response(serializer.data)
    
    def get_session_by_id(self, session_id):
        
        try:
            session_db = Sessions.objects.get(session_id=session_id)
            return session_db
        except Sessions.DoesNotExist:
            raise Http404('Session does not exist.')
    
    def post(self, request):
        
        serializer = SessionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, session_id):
        
        session = self.get_session_by_id(session_id)
        serializer = SessionsSerializer(session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    