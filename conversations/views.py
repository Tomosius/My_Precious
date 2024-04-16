from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Subquery, OuterRef
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

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


class ConversationDetailView(LoginRequiredMixin, DetailView, FormView):
    """
    Class-based view for displaying messages in a specific conversation
    and allowing the user to send a message within this conversation.

    Inherits from:
    - LoginRequiredMixin: Ensures that the user is logged in.
    - DetailView: Provides the details of a specific conversation.
    - FormView: Handles the submission of the message form.

    Attributes:
    - model: Specifies the Conversation model to be used.
    - form_class: Specifies the form for sending messages.
    - template_name: The name of the template to use.
    - context_object_name: The name of the context object in the template.
    """

    model = Conversation
    form_class = MessageForm
    template_name = 'conversation_detail_page.html'
    context_object_name = 'conversation'

    def __init__(self, **kwargs):
        """
        Initializes the ConversationDetailView instance.

        Args:
        - **kwargs: Keyword arguments for initialization.
        """
        super().__init__(**kwargs)  # Corrected to properly unpack kwargs
        self.object = None  # Initialize the object attribute

    def get_success_url(self):
        """
        Defines the URL to redirect to on successful form submission.

        Returns:
        - URL as a string to redirect back to the conversation detail view.
        """
        return reverse('conversations:conversation_detail',
                       kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template.

        Args:
        - **kwargs: Keyword arguments containing context data.

        Returns:
        - The context dictionary with additional entries.
        """
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.order_by('created_at')
        if 'form' not in context:
            context[
                'form'] = self.get_form()  # Adds the form to the context if
            # not already present
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, processing the message form.

        Args:
        - request: The HTTP request object.
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - An HttpResponseRedirect on success, or the form with errors on
        failure.
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Processes a valid form, creating a new message in the conversation.

        Args:
        - form: The validated form instance.

        Returns:
        - An HttpResponseRedirect to the success URL.
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

    ListView for rendering a list of objects.
    """
    model = Conversation
    context_object_name = 'conversations'
    template_name = 'conversations_list.html'

    def get_queryset(self):
        """
        Overrides the default queryset to return conversations for the
        current user only, ordered by the most recent message sent time.

        Returns:
        - QuerySet: The filtered queryset of conversations for the
        logged-in user, ordered by the most recent message update time.
        """
        # Subquery to get the most recent message update time for each
        # conversation
        latest_message_times = Message.objects.filter(
            conversation=OuterRef('pk')
        ).order_by('-created_at').values('created_at')[:1]

        # Query to retrieve conversations for the current user, ordered by
        # the most recent message update time
        return Conversation.objects.filter(
            participants=self.request.user
        ).annotate(
            latest_message_time=Subquery(latest_message_times)
        ).order_by('-latest_message_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversations = context['conversations']

        for conversation in conversations:
            # Prefetch the last three messages for each conversation
            last_three_messages = Message.objects.filter(
                conversation=conversation
            ).order_by('-created_at')[:3]

            # Attaching the last three messages directly to each conversation
            # object
            conversation.last_three_messages = last_three_messages

        return context
