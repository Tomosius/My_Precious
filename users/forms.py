from cloudinary.forms import CloudinaryFileField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, SocialMediaLink, Language


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Required. Add a valid "
                                                       "email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1",
                  "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    user_photo = CloudinaryFileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )
    first_name = forms.CharField(
        label='First Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        # Apply class here
    )
    last_name = forms.CharField(
        label='Last Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        # Standard form-control class
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'user_photo', 'address',
                  'mobile_number', 'biography', 'website', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('user_photo', css_class='mb-2'),
            'address',
            'mobile_number',
            'biography',
            'website',
            'date_of_birth',
            'gender',
        )


class UserCredentialsForm(forms.ModelForm):
    """Form for updating user's username and email."""

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCredentialsForm, self).__init__(*args, **kwargs)
        self.fields[
            'username'].help_text = ('Required. 150 characters or fewer. '
                                     'Letters, digits and @/./+/-/_ only.')


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom form for user password change."""

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = None


class SocialMediaLinkForm(forms.ModelForm):
    """Form for creating or updating social media links."""

    class Meta:
        model = SocialMediaLink
        fields = ['name', 'url']


class LanguageForm(forms.ModelForm):
    """Form for creating or updating languages."""

    class Meta:
        model = Language
        fields = ['language']
