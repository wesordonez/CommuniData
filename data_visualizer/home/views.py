from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from home.forms import ContactForm

# Removing CSRF token from the form for testing purposes. This needs to be removed later.
from django.views.decorators.csrf import csrf_exempt


def home(request):
    """Home view function.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        HttpResponse: The HTTP response.
    
    """
    return render(request, 'home/home.html')


@csrf_exempt
def contact(request):
    """Contact view function.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        HttpResponse: The HTTP response.
    
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
            return HttpResponse('Invalid form submission.')
    else:
        form = ContactForm()
    return render(request, 'home/home.html', {'form': form})
    