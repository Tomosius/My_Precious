from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .forms import MessageForm
from .models import Conversation, Message


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
        Processes the valid form. Creates or updates the conversation and
        sends the message.

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


from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse

class ConversationDetailView(LoginRequiredMixin, DetailView, FormView):
    """
    Updated class-based view for displaying messages in a specific conversation
    and allowing the user to send a message within this conversation.
    """
    model = Conversation
    form_class = MessageForm  # Use the existing MessageForm
    template_name = 'conversation_detail.html'
    context_object_name = 'conversation'

    def get_success_url(self):
        """
        Redirects back to the same conversation detail view on successful message submission.
        """
        return reverse('conversations:conversation_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template, specifically the messages in the conversation
        and the message form.
        """
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.order_by('created_at')
        if 'form' not in context:  # Add the message form to the context
            context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, allowing users to send messages from the conversation detail view.
        """
        self.object = self.get_object()  # Get the current conversation object
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Processes the valid form submission, creating a new message within the conversation.
        """
        message = form.save(commit=False)
        message.sender = self.request.user
        message.conversation = self.object
        message.save()
        return HttpResponseRedirect(self.get_success_url())



class ConversationListView(LoginRequiredMixin, ListView):
    """
    Class-based view for displaying a list of conversations for the current
    user.

    Inherits from LoginRequiredMixin to ensure user authentication and
    ListView for rendering a list of objects.
    """
    model = Conversation
    context_object_name = 'conversations'
    template_name = 'conversations_list.html'

    def get_queryset(self):
        """
        Overrides the default queryset to return conversations for the
        current user only.

        Returns: - QuerySet: The filtered queryset of conversations for the
        logged-in user.
        """
        return Conversation.objects.filter(
            participants=self.request.user).order_by('-updated_at')

