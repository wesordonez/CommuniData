from django.urls import path
from .views import ConsultantAPIView, BipAPIView, BuildingsAPIView, ContactsAPIView, BusinessAPIView, ClientsAPIView, SessionAPIView

urlpatterns = [
    path('consultants/', ConsultantAPIView.as_view(), name='consultants'),
    path('consultants/<int:consultant_id>/', ConsultantAPIView.as_view(), name='consultant'),
    path('bips/', BipAPIView.as_view(), name='bips'),
    path('bips/<int:bip_id>/', BipAPIView.as_view(), name='bip'),
    path('buildings/', BuildingsAPIView.as_view(), name='buildings'),
    path('contacts/', ContactsAPIView.as_view(), name='contacts'),
    path('contacts/<int:contact_id>/', ContactsAPIView.as_view(), name='contact'),
    path('business/', BusinessAPIView.as_view(), name='business'),
    path('business/<int:business_id>/', BusinessAPIView.as_view(), name='business'),
    path('clients/', ClientsAPIView.as_view(), name='clients'),
    path('clients/<int:client_id>/', ClientsAPIView.as_view(), name='client'),
    path('sessions/', SessionAPIView.as_view(), name='sessions'),
    path('sessions/<int:session_id>/', SessionAPIView.as_view(), name='session'),
]
