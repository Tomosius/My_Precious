from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversation, Message
from django.contrib.auth.models import User
from django.db.models import Q
from users.models import UserProfile

from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversation, Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def send_message(request, recipient_username):
    """
    Handles the sending of a message to another user, checking for an existing conversation or starting a new one.

    Args:
    - request: HttpRequest object.
    - recipient_username: The username of the message recipient.

    Returns:
    - HttpResponse object redirecting to the conversation view.
    """
    sender = request.user
    recipient = get_object_or_404(User, username=recipient_username)

    # Attempt to retrieve an existing conversation between the sender and recipient
    conversation = Conversation.objects.filter(
        participants=sender
    ).filter(
        participants=recipient
    ).first()

    # If no existing conversation, create a new one and add both participants
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(sender, recipient)

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(conversation=conversation, sender=sender, text=message_text)
            # Redirect to the specific conversation view using the conversation ID
            return redirect('conversations:conversation_detail', conversation_id=conversation.id)

    # For GET requests or if the message text is empty, show the form again
    return render(request, 'message_form.html', {'recipient': recipient})

# Assume 'conversation_detail' is a view that you will define,
# which shows the messages in a specific conversation

# Assume 'conversation_detail' is a view that you will define,
# which shows the messages in a specific conversation
def conversation_detail(request, conversation_id):
    """
    Fetches and displays the messages in a specific conversation.

    Args:
    - request: HttpRequest object.
    - conversation_id: The ID of the conversation to display.

    Returns:
    - HttpResponse object rendering the conversation detail template.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).order_by('created_at')

    return render(request, 'conversation_detail.html', {'conversation': conversation, 'messages': messages})


def conversation_list(request):
    """
    Fetches and displays the list of conversations for the current user.

    Args:
    - request: HttpRequest object.

    Returns:
    - HttpResponse object rendering the conversations list template.
    """
    user = request.user
    conversations = Conversation.objects.filter(participants=user).order_by('-updated_at')

    return render(request, 'conversations_list.html', {'conversations': conversations})
