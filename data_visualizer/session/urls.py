from django.urls import path
from .views import ConsultantAPIView, BipAPIView

urlpatterns = [
    path('consultants/', ConsultantAPIView.as_view(), name='consultants'),
    path('bips/', BipAPIView.as_view(), name='bips')
]
