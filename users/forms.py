from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, SocialMediaLink, Language


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Add a valid '
                                                      'email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_photo', 'address', 'mobile_number', 'biography',
                  'website', 'date_of_birth', 'gender']


class SocialMediaLinkForm(forms.ModelForm):
    class Meta:
        model = SocialMediaLink
        fields = ['name', 'url']
        extra = 1


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language']
        extra = 1
