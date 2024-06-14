from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Message, PrivateChatRequest, PrivateChat
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import GroupForm, MessageForm, PrivateMessageForm

# API
#from wallet.models import Transaction
#from .serializers import GroupSerializer, MessageSerializer
#from rest_framework.response import Response
#from rest_framework import viewsets
#from rest_framework.decorators import action

# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

#     @action(detail=True, methods=['post'])
#     def join(self, request, pk=None):
#         group = self.get_object()
#         user = request.user
#         if user.coins > 0:
#             group.members.add(user)
#             user.coins -= 1
#             user.save()
#             Transaction.objects.create(user=user, amount=-1, description='Joined group')
#             return Response({'status': 'joined group'})
#         return Response({'status': 'insufficient coins'}, status=400)

# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer





User = get_user_model()


# home page (index.html)
def home_view(request):
    return render(request, 'index.html')

# page for showing all groups 
@login_required
def groups(request):
    groups = Group.objects.all()
    return render(request, 'groups.html', {'groups': groups})

# page for each group when join
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    members = group.members.all()
    messages = Message.objects.filter(group=group).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.group = group
            message.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = MessageForm()

    context = {
        'group': group,
        'members': members,
        'messages': messages,
        'form': form,
    }
    return render(request, 'group_detail.html', context)
    
# Create group
@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            group.members.add(request.user)
            group.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})


# join a group
@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.add(request.user)
    return redirect('group_detail', group_id=group.id)



@login_required
def private_chat_list(request):
    private_chats = PrivateChat.objects.filter(participants=request.user)
    return render(request, 'private_chat_list.html', {'private_chats': private_chats})

@login_required
def start_private_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if other_user == request.user:
        return redirect('private_chat_list')
    
    chat, created = PrivateChat.objects.get_or_create(participants=request.user)
    chat.participants.add(other_user)
    
    return redirect('private_chat_detail', chat_id=chat.id)

@login_required
def private_chat_detail(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id)
    if request.user not in chat.participants.all():
        return redirect('private_chat_list')

    if request.method == 'POST':
        form = PrivateMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chat = chat
            message.receiver = chat.participants.exclude(id=request.user.id).first()
            message.save()
            return redirect('private_chat_detail', chat_id=chat.id)
    else:
        form = PrivateMessageForm()

    messages = chat.messages.order_by('timestamp')
    return render(request, 'private_chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'form': form,
    })

@login_required
def send_private_chat_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if request.user == receiver:
        return redirect('private_chat_list')
    
    PrivateChatRequest.objects.get_or_create(sender=request.user, receiver=receiver)
    return redirect('private_chat_list')

@login_required
def handle_private_chat_request(request, request_id, action):
    chat_request = get_object_or_404(PrivateChatRequest, id=request_id)
    if chat_request.receiver != request.user:
        return redirect('private_chat_list')

    if action == 'accept':
        chat_request.status = 'accepted'
        chat, created = PrivateChat.objects.get_or_create(participants=request.user)
        chat.participants.add(chat_request.sender)
    elif action == 'decline':
        chat_request.status = 'declined'

    chat_request.save()
    return redirect('private_chat_list')

@login_required
def private_chat_requests(request):
    received_requests = PrivateChatRequest.objects.filter(receiver=request.user)
    sent_requests = PrivateChatRequest.objects.filter(sender=request.user)
    return render(request, 'private_chat_requests.html', {
        'received_requests': received_requests,
        'sent_requests': sent_requests
    })

@login_required
def private_chats(request):
    chats = PrivateChat.objects.filter(participants=request.user)
    return render(request, 'private_chats.html', {
        'chats': chats
    })

@login_required
def private_chat(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id, participants=request.user)
    messages = chat.messages.order_by('timestamp')
    return render(request, 'private_chat.html', {
        'chat': chat,
        'messages': messages
    })

@login_required
def accept_request(request, request_id):
    chat_request = get_object_or_404(PrivateChatRequest, id=request_id, receiver=request.user)
    chat_request.status = 'accepted'
    chat_request.save()
    return redirect('private_chat_requests')

@login_required
def decline_request(request, request_id):
    chat_request = get_object_or_404(PrivateChatRequest, id=request_id, receiver=request.user)
    chat_request.status = 'declined'
    chat_request.save()
    return redirect('private_chat_requests')