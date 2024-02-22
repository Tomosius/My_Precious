from django import forms
from django.forms.widgets import ClearableFileInput
from .models import LostPost, FoundPost, LostPhoto, FoundPhoto
from cloudinary.forms import CloudinaryFileField


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if data:
            return [super(MultipleFileField, self).clean(file, initial) for file
                    in data]
        else:
            return super(MultipleFileField, self).clean(data, initial)


class FileFieldForm(forms.Form):
    file_field = MultipleFileField(required=False, widget=MultipleFileInput(
        attrs={'multiple': True}), label="Upload photo(s)")


class BasePostForm(forms.ModelForm):
    event_date = forms.DateField(label="Event Date",
                                 widget=forms.DateInput(attrs={'type': 'date'}),
                                 help_text="Select the date of the event.")
    title = forms.CharField(label="Title", max_length=255)
    description = forms.CharField(label="Description", widget=forms.Textarea)


    class Meta:
        fields = ['title', 'description', 'latitude', 'longitude', 'event_date',
                  'date_uncertainty_days']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }



class FoundPostForm(BasePostForm):
    class Meta(BasePostForm.Meta):
        model = FoundPost


class LostPostForm(BasePostForm):
    class Meta(BasePostForm.Meta):
        model = LostPost


