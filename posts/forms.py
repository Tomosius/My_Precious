from django import forms
from django.forms.widgets import ClearableFileInput

from .models import LostPost, FoundPost
from django.core.exceptions import ValidationError
from django.utils import timezone


class MultipleFileInput(ClearableFileInput):
    """
    A custom widget to allow multiple file selections in file input fields.
    Inherits from Django's ClearableFileInput to add support for multiple
    file selection.
    """
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """
    A custom form field for handling multiple file uploads.
    Overrides the default FileField to use the MultipleFileInput widget.
    """
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        """
        Cleans the data for this field and returns a list of cleaned files.

        Args:
            data: The uploaded file(s).
            initial: Initial data for field.

        Returns:
            List of cleaned files.
        """
        if data:
            return [super().clean(file, initial) for file in data]
        else:
            return super().clean(data, initial)


class FileFieldForm(forms.Form):
    """
    A form for handling multiple file uploads.
    """
    file_field = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={'multiple': True}),
        label="Upload photo(s)"
    )


class BasePostForm(forms.ModelForm):
    """
    An abstract base form for creating and updating 'Post' instances.
    Defines common fields and widgets used across different types of posts.
    """
    event_date = forms.DateField(
        label="Event Date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select the date of the event."
    )
    title = forms.CharField(label="Title", max_length=255)
    description = forms.CharField(label="Description", widget=forms.Textarea(
        attrs={'rows': 4, 'cols': 15}))

    class Meta:
        abstract = True
        fields = ['title', 'description', 'latitude', 'longitude', 'event_date',
                  'date_uncertainty_days']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_event_date(self):
        """
        Validates that the event_date is not later than the current date.
        Raises ValidationError if the date is in the future.
        """
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date > timezone.now().date():
            raise ValidationError("The event date cannot be in the future.")
        return event_date


class FoundPostForm(BasePostForm):
    """
    A form for creating or updating 'FoundPost' instances.
    Inherits from BasePostForm and sets the specific model to FoundPost.
    """

    class Meta(BasePostForm.Meta):
        model = FoundPost


class LostPostForm(BasePostForm):
    """
    A form for creating or updating 'LostPost' instances.
    Inherits from BasePostForm and sets the specific model to LostPost.
    """

    class Meta(BasePostForm.Meta):
        model = LostPost
