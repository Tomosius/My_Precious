from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm


# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')  # Redirect to
            # the logged-in user's profile
        else:
            messages.error(request,
                           'Invalid login credentials. Please try again.')
    return render(request, 'user_login.html')


# User Logout
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()  # UserProfile will be created by the signal
            messages.success(request, 'Account created successfully.')
            return redirect('users:user_login')
    else:
        user_form = UserRegisterForm()
    return render(request, 'user_register.html', {'form': user_form})
