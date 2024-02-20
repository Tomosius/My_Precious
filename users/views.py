from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileForm, UserCredentialsForm, CustomPasswordChangeForm, LanguageForm, \
    SocialMediaLinkForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Language, SocialMediaLink, UserProfile


def user_login(request):
    """
    View for handling user login.
    Authenticates user and redirects to home page on success.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')  # Ensure 'home' is correctly defined in
            # your URLconf
        else:
            messages.error(request, 'Invalid login credentials. Please try '
                                    'again.')
    return render(request, 'user_login.html')


@login_required
def user_logout(request):
    """
    Logs out the user and redirects to home page.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')  # Ensure 'home' is correctly defined in your
    # URLconf


def user_register(request):
    """
    Handles new user registration.
    On POST, validates form and creates a new user on success.
    """
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()  # UserProfile creation is handled via signal
            messages.success(request, 'Account created successfully.')
            return redirect('user_login')
    else:
        user_form = UserRegisterForm()
    return render(request, 'user_register.html', {'form': user_form})


@login_required
def user_profile(request, username):
    """
    Displays the user profile for the given username.
    """
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    context = {'user': user, 'user_profile': user_profile}
    return render(request, 'user_profile.html', context)


@login_required
def update_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)  # This ensures a profile exists
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect('user_profile', username=user.username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile_update.html', {'profile_form': form})


@login_required
def update_credentials(request):
    """
    Allows users to update their credentials (username and email).
    """
    if request.method == 'POST':
        user_form = UserCredentialsForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your credentials have been updated '
                                      'successfully.')
            return redirect('user_profile', username=request.user.username)
    else:
        user_form = UserCredentialsForm(instance=request.user)
    return render(request, 'credentials_update.html', {'user_form': user_form})


@login_required
def change_password(request):
    """
    Allows the user to change their password.
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents user from
            # being logged out after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile', username=request.user.username)
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})



@login_required
def add_language(request):
    """
    Allows users to add a language to their profile via AJAX.
    """
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = form.save(commit=False)
            language.user_profile = request.user.profile  # Ensure this matches your user profile relation
            language.save()
            return JsonResponse({
                'language_id': language.id,
                'language_name': language.language  # Make sure 'language' attribute exists in your model
            })
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)





@login_required
def add_social_media_link(request):
    """
    Allows users to add a social media link to their profile via AJAX.
    """
    if request.method == 'POST':
        form = SocialMediaLinkForm(request.POST)
        if form.is_valid():
            social_media_link = form.save(commit=False)
            social_media_link.user_profile = request.user.profile  # Ensure this matches your user profile relation
            social_media_link.save()
            # Assuming your model has 'name' and 'url' fields you want to return
            return JsonResponse({
                'success': True,
                'link_id': social_media_link.id,
                'link_name': social_media_link.name,
                'link_url': social_media_link.url
            })
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)



def delete_language(request, language_id):
    if request.method == 'POST':
        try:
            language = Language.objects.get(id=language_id)
            language.delete()
            return JsonResponse({'success': True, 'message': 'Language deleted successfully.'})
        except Language.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'}, status=400)


@login_required
def delete_social_media_link(request, link_id):
    """
    Allows users to delete a social media link from their profile.
    """
    # Ensure the user is authenticated and is using POST method
    if request.user.is_authenticated and request.method == 'POST':
        link = SocialMediaLink.objects.get(id=link_id)
        link.delete()
        # Return a JSON response indicating success
        return JsonResponse({'success': True, 'message': 'Social media link deleted successfully.'})
    else:
        # Return a JSON response indicating failure
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'}, status=400)


@login_required
def combined_update_user_profile(request):
    """
    Combined view for updating user profile, credentials, password,
    managing languages, and social media links.
    """
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Initialize forms
    profile_form = UserProfileForm(instance=profile)
    user_form = UserCredentialsForm(instance=user)
    password_form = CustomPasswordChangeForm(user=user)
    language_form = LanguageForm()
    social_media_link_form = SocialMediaLinkForm()

    # pulling from database exsisting languages and socila networks
    current_languages = Language.objects.filter(user_profile=profile)
    current_social_media_links = SocialMediaLink.objects.filter(user_profile=profile)

    # Check which form was submitted
    if request.method == 'POST':
        if 'profile_form' in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Your profile was successfully updated!")
                return redirect('users:user_profile', username=user.username)

        elif 'user_form' in request.POST:
            user_form = UserCredentialsForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your credentials have been updated successfully.')
                return redirect('users:user_profile', username=user.username)

        elif 'password_form' in request.POST:
            password_form = CustomPasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Prevents logout
                messages.success(request, 'Your password was successfully updated!')
                return redirect('users:user_profile', username=user.username)

        elif 'language_form' in request.POST:
            language_form = LanguageForm(request.POST)
            if language_form.is_valid():
                language = language_form.save(commit=False)
                language.user_profile = profile
                language.save()
                messages.success(request, 'Language added successfully.')
                return redirect('users:user_profile', username=user.username)

        elif 'social_media_link_form' in request.POST:
            social_media_link_form = SocialMediaLinkForm(request.POST)
            if social_media_link_form.is_valid():
                social_media_link = social_media_link_form.save(commit=False)
                social_media_link.user_profile = profile
                social_media_link.save()
                messages.success(request, 'Social media link added successfully.')
                return redirect('users:user_profile', username=user.username)

    # Handle language and link deletion separately if needed
    # Example: Check for 'delete_language' or 'delete_social_media_link' in request.GET
    # and process accordingly

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'password_form': password_form,
        'language_form': language_form,
        'social_media_link_form': social_media_link_form,
        'current_languages': current_languages,
        'current_social_media_links': current_social_media_links,
        # Consider adding languages and social media links to context for management
    }

    return render(request, 'profile_update.html', context)
