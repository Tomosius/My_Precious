from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from conversations.forms import MessageForm
from conversations.models import Conversation, Message
from posts.models import LostPost, FoundPost
from .forms import UserCredentialsForm, CustomPasswordChangeForm, \
    UserProfileForm
from .forms import UserRegisterForm, LanguageForm, \
    SocialMediaLinkForm
from .models import Language, SocialMediaLink
from .models import UserProfile


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UserRegisterForm

class UserLoginView(LoginView):
    template_name = 'user_login.html'
    next_page = reverse_lazy('home')  # Assuming 'home' is the name of your homepage URL

class UserRegisterView(FormView):
    template_name = 'user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:user_login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



@login_required
def user_logout(request):
    """
    Logs out the user and redirects to home page.
    """
    logout(request)
    return redirect('home')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm

class UpdateProfileView(LoginRequiredMixin, View):
    def get_object(self):
        user = self.request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request, *args, **kwargs):
        form = UserProfileForm(instance=self.get_object())
        return render(request, 'profile_update.html', {'profile_form': form})

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect('users:user_profile', username=request.user.username)
        else:
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
            return redirect('users:user_profile',
                            username=request.user.username)
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
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:user_profile',
                            username=request.user.username)
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
            language.user_profile = request.user.profile
            language.save()
            return JsonResponse({
                'language_id': language.id,
                'language_name': language.language
            })
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors},
                                status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'},
                        status=400)


@login_required
def add_social_media_link(request):
    """
    Allows users to add a social media link to their profile via AJAX.
    """
    if request.method == 'POST':
        form = SocialMediaLinkForm(request.POST)
        if form.is_valid():
            social_media_link = form.save(commit=False)
            social_media_link.user_profile = request.user.profile
            social_media_link.save()
            return JsonResponse({
                'success': True,
                'link_id': social_media_link.id,
                'link_name': social_media_link.name,
                'link_url': social_media_link.url
            })
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors},
                                status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'},
                        status=400)


def delete_language(request, language_id):
    if request.method == 'POST':
        try:
            language = Language.objects.get(id=language_id)
            language.delete()
            return JsonResponse(
                {'success': True, 'message': 'Language deleted successfully.'})
        except Language.DoesNotExist:
            return JsonResponse({'success': False,
                                 'message': 'An error occurred. Please try '
                                            'again.'},
                                status=400)


@login_required
def delete_social_media_link(request, link_id):
    """
    Allows users to delete a social media link from their profile.
    """
    if request.user.is_authenticated and request.method == 'POST':
        link = SocialMediaLink.objects.get(id=link_id)
        link.delete()
        return JsonResponse({'success': True,
                             'message': 'Social media link deleted '
                                        'successfully.'})
    else:
        return JsonResponse({'success': False,
                             'message': 'An error occurred. Please try again.'},
                            status=400)


@login_required
def combined_update_user_profile(request):
    """
    Combined view for updating user profile, credentials, password,
    managing languages, and social media links.
    """
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    profile_form = UserProfileForm(instance=profile)
    user_form = UserCredentialsForm(instance=user)
    password_form = CustomPasswordChangeForm(user=user)
    language_form = LanguageForm()
    social_media_link_form = SocialMediaLinkForm()

    current_languages = Language.objects.filter(user_profile=profile)
    current_social_media_links = SocialMediaLink.objects.filter(
        user_profile=profile)

    if request.method == 'POST':
        if 'profile_form' in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES,
                                           instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request,
                                 "Your profile was successfully updated!")
                return redirect('users:user_profile', username=user.username)

        elif 'user_form' in request.POST:
            user_form = UserCredentialsForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request,
                                 'Your credentials have been updated '
                                 'successfully.')
                return redirect('users:user_profile', username=user.username)

        elif 'password_form' in request.POST:
            password_form = CustomPasswordChangeForm(user=user,
                                                     data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Prevents logout
                messages.success(request,
                                 'Your password was successfully updated!')
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
                messages.success(request,
                                 'Social media link added successfully.')
                return redirect('users:user_profile', username=user.username)

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'password_form': password_form,
        'language_form': language_form,
        'social_media_link_form': social_media_link_form,
        'current_languages': current_languages,
        'current_social_media_links': current_social_media_links,
    }

    return render(request, 'profile_update.html', context)


@login_required
def list_users(request):
    users = User.objects.select_related('profile').all()
    return render(request, 'user_list.html', {'users': users})




@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = user.profile
    is_owner = request.user == user

    user_lost_posts = LostPost.objects.filter(user=user)
    user_found_posts = FoundPost.objects.filter(user=user)
    posts = list(user_lost_posts) + list(user_found_posts)

    conversations = Conversation.objects.none()

    # Moved inside the POST request check as it's only needed there
    if request.method == 'POST':
        messages_form = MessageForm(request.POST)
        if messages_form.is_valid() and not is_owner:
            message_text = messages_form.cleaned_data['text']
            conversation = Conversation.objects.filter(
                participants=user).filter(participants=request.user).first()
            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.add(user, request.user)
            Message.objects.create(conversation=conversation,
                                   sender=request.user, text=message_text)
            return redirect('users:user_profile',
                            username=username)  # Redirect back to the same profile page
        else:
            # Log form errors if the form is not valid
            print(messages_form.errors)
    else:
        # Initialize the form without POST data for GET requests
        messages_form = MessageForm()

    if not is_owner:
        conversations = Conversation.objects.filter(participants=user).filter(
            participants=request.user).distinct().prefetch_related(
            'messages').order_by('-updated_at')

    context = {
        'user_profile': user_profile,
        'user': user,
        'posts': posts,
        'is_owner': is_owner,
        'conversations': conversations,
        'messages_form': messages_form,  # Pass the form to the template
    }

    return render(request, 'user_profile.html', context)










