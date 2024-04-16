from django.urls import path
from .views import ConsultantAPIView, BipAPIView

urlpatterns = [
    path('consultants/', ConsultantAPIView.as_view(), name='consultants'),
    path('consultants/<int:consultant_id>/', ConsultantAPIView.as_view(), name='consultant'),
    path('bips/', BipAPIView.as_view(), name='bips'),
    path('bips/<int:bip_id>/', BipAPIView.as_view(), name='bip'),
]
