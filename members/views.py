from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import registerUserForm
# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'An error has occur')
            return redirect(login_user)
    else:
        
        return render(request, 'members/login.html', {})
    


def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = registerUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        # If form is not valid, fall through to re-render the form with errors
    else:
        form = registerUserForm()
    
    # If not POST or form is invalid, render the form with any errors
    return render(request, 'members/register.html', {'form': form})

