from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('payments/', views.payments, name='payments'),
    path('login/', LoginView.as_view(), name='login'),
    # path('dashboard/', views.dashboard, name='dashboard'),
]
