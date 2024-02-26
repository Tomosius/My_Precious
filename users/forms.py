from cloudinary.forms import CloudinaryFileField
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import SocialMediaLink, Language
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False,
                             help_text="Required. Add a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    user_photo = CloudinaryFileField(required=False)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'user_photo', 'address',
                  'mobile_number', 'biography', 'website', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserCredentialsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            'username'].help_text = ('Required. 150 characters or fewer. '
                                     'Letters, digits and @/./+/-/_ only.')
        for field_name in ['username', 'email']:
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].help_text = None


class SocialMediaLinkForm(forms.ModelForm):
    class Meta:
        model = SocialMediaLink
        fields = ['name', 'url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].widget.attrs.update({'class': 'form-control'})


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].widget.attrs.update({'class': 'form-control'})
