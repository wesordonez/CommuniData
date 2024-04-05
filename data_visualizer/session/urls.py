from django.urls import path
from .views import ConsultantAPI

urlpatterns = [
    path('consultants/', ConsultantAPI.as_view(), name='consultants'),
]
