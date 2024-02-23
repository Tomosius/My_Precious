from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    """
    Form for sending a message to another user.
    """

    class Meta:
        model = Message
        fields = ['text']
        labels = {'text': 'Message'}
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
