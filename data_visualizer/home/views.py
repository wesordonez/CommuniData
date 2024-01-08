from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Hello, world. You are at the home index.</h1>')

# Create your views here.
