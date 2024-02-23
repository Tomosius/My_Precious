from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from .forms import MessageForm
from .models import Conversation, Message
from django.contrib.auth.models import User

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class SendMessageView(LoginRequiredMixin, FormView):
    """
    Class-based view to handle sending of messages between users.

    Inherits from LoginRequiredMixin to ensure the user is authenticated and
    FormView for handling the message form submission.
    """
    form_class = MessageForm
    template_name = 'message_form.html'

    def form_valid(self, form):
        """
        Processes the valid form. Creates or updates the conversation and sends the message.

        Args:
        - form: The validated form instance.

        Returns:
        - HttpResponse: Redirects to the conversation detail view on success.
        """
        recipient_username = self.kwargs['recipient_username']
        sender = self.request.user
        recipient = get_object_or_404(User, username=recipient_username)

        conversation = Conversation.objects.filter(participants=sender).filter(
            participants=recipient).first()
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(sender, recipient)

        message_text = form.cleaned_data['text']
        Message.objects.create(conversation=conversation, sender=sender,
                               text=message_text)

        return redirect('conversations:conversation_detail',
                        pk=conversation.id)




class ConversationDetailView(LoginRequiredMixin, DetailView):
    """
    Class-based view for displaying messages in a specific conversation.

    Inherits from LoginRequiredMixin to ensure user authentication and
    DetailView for rendering a single object.
    """
    model = Conversation
    context_object_name = 'conversation'
    template_name = 'conversation_detail.html'

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template, specifically the messages in the conversation.

        Returns:
        - context: The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(
            conversation=self.object).order_by('created_at')
        return context


class ConversationListView(LoginRequiredMixin, ListView):
    """
    Class-based view for displaying a list of conversations for the current user.

    Inherits from LoginRequiredMixin to ensure user authentication and
    ListView for rendering a list of objects.
    """
    model = Conversation
    context_object_name = 'conversations'
    template_name = 'conversations_list.html'

    def get_queryset(self):
        """
        Overrides the default queryset to return conversations for the current user only.

        Returns:
        - QuerySet: The filtered queryset of conversations for the logged-in user.
        """
        return Conversation.objects.filter(
            participants=self.request.user).order_by('-updated_at')




