from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from home.forms import ContactForm


def home(request):
    return render(request, 'home/home.html')

class ContactFromView(ContactForm):
    form_class = ContactForm
    template_name = 'home/contact_form.html'    
    success_url = '/'
    
    def form_valid(self, form):
        print("success")
        return super().form_valid(form)
    