from django.contrib.auth import login
from django.shortcuts import render, redirect
from formulations.forms import RegistrationForm

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) # Log the new user in immediately after registration
            return redirect('home')
    else:
        form = RegistrationForm() # An empty form for GET requests

    return render(request, 'registration/register.html', {'form': form})