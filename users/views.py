from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserProfileForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from .models import UserProfile

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')  # Adjust the redirect as needed
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    return render(request, 'user_login.html')

# User Logout
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')  # Adjust the redirect as needed

# User Registration
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

# Display User Profile
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    return render(request, 'user_profile.html', context)

# Update User Profile
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'profile_update.html', {'form': form})

