from django.urls import path
from .views import ConsultantAPIView

urlpatterns = [
    path('consultants/', ConsultantAPIView.as_view(), name='consultants'),
]
