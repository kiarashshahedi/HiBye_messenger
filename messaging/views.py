from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Message, PrivateChatRequest, PrivateChat, Block
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import GroupForm, MessageForm, PrivateMessageForm, ReportForm
from django.contrib import messages

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
            if request.user.coins >= 1:
                group = form.save(commit=False)
                group.created_by = request.user  # Ensure the created_by field is set
                group.save()
                group.members.add(request.user)  # Add the creator to the group members
                request.user.coins -= 1
                request.user.save()
                messages.success(request, f'Group created successfully! 1 coin has been deducted. You have {request.user.coins} coins left.')
                return redirect('group_detail', group_id=group.id)
            else:
                messages.error(request, 'You do not have enough coins to create a group.')
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})


# join a group
@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user.coins >= 1:
        group.members.add(request.user)
        request.user.coins -= 1
        request.user.save()
        return redirect('group_detail', group_id=group_id)
    else:
        messages.error(request, "You do not have enough coins to join this group.")
        return redirect('groups')
    
@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user in group.members.all():
        group.members.remove(request.user)
        messages.success(request, f'You have left the group {group.name}.')
    else:
        messages.error(request, 'You are not a member of this group.')
    return redirect('groups')
    
'''   Privet chats     '''

@login_required
def private_chat_list(request):
    private_chats = PrivateChat.objects.filter(participants=request.user)
    return render(request, 'private_chat_list.html', {'private_chats': private_chats})

@login_required
def start_private_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if other_user == request.user:
        return redirect('private_chat_list')
    
    chat, created = PrivateChat.objects.get_or_create()
    chat.participants.add(request.user, other_user)
    
    return redirect('private_chat_detail', chat_id=chat.id)

@login_required
def private_chat_detail(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id)
    if request.user not in chat.participants.all():
        return redirect('private_chat_list')

    other_participant = chat.participants.exclude(id=request.user.id).first()
    blocked_users = Block.objects.filter(blocker=request.user).values_list('blocked', flat=True)

    if other_participant.id in blocked_users:
        messages_list = []
        form = None
        messages.error(request, "You have blocked this user.")
        return render(request, 'private_chat_detail.html', {
            'chat': chat,
            'messages_list': messages_list,
            'form': form,
            'other_participant': other_participant,
            'is_blocked': True,
        })

    if request.method == 'POST':
        form = PrivateMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chat = chat
            message.receiver = other_participant
            message.save()
            return redirect('private_chat_detail', chat_id=chat.id)
    else:
        form = PrivateMessageForm()

    messages_list = chat.messages.order_by('timestamp')
    return render(request, 'private_chat_detail.html', {
        'chat': chat,
        'messages_list': messages_list,
        'form': form,
        'other_participant': other_participant,
        'is_blocked': False,
    })


@login_required
def handle_private_chat_request(request, request_id, action):
    chat_request = get_object_or_404(PrivateChatRequest, id=request_id)
    if chat_request.receiver != request.user:
        return redirect('private_chat_list')

    if action == 'accept':
        chat_request.status = 'accepted'
        chat, created = PrivateChat.objects.get_or_create(participants=request.user)
        chat.participants.add(chat_request.sender)

        # Deduct coins from both users
        if chat_request.sender.coins >= 1 and request.user.coins >= 1:
            chat_request.sender.coins -= 1
            request.user.coins -= 1
            chat_request.sender.save()
            request.user.save()
        else:
            messages.error(request, "One of the users does not have enough coins to start a private chat.")
            return redirect('private_chat_requests')

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
def private_chat(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id, participants=request.user)
    messages = chat.messages.order_by('timestamp')
    return render(request, 'private_chat.html', {
        'chat': chat,
        'messages': messages
    })
    
@login_required
def send_private_chat_request(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        receiver = get_user_model().objects.filter(id=receiver_id).first()
        if not receiver:
            return redirect('private_chat_requests')  # or handle the error appropriately
        PrivateChatRequest.objects.get_or_create(sender=request.user, receiver=receiver)
        return redirect('private_chat_requests')
    else:
        users = get_user_model().objects.exclude(id=request.user.id)
        return render(request, 'send_private_chat_request.html', {'users': users})
    
@login_required
def accept_request(request, request_id):
    chat_request = get_object_or_404(PrivateChatRequest, id=request_id, receiver=request.user)
    chat_request.status = 'accepted'
    chat_request.save()
    
    # Create a private chat if not exists
    chat, created = PrivateChat.objects.get_or_create()
    chat.participants.add(chat_request.sender, request.user)
    
    return redirect('private_chat_requests')

@login_required
def decline_request(request, request_id):
    chat_request = get_object_or_404(PrivateChatRequest, id=request_id, receiver=request.user)
    chat_request.status = 'declined'
    chat_request.save()
    return redirect('private_chat_requests')




@login_required
def block_user(request, user_id):
    blocked_user = get_object_or_404(User, id=user_id)
    Block.objects.get_or_create(blocker=request.user, blocked=blocked_user)
    messages.success(request, f'You have blocked {blocked_user.username}.')
    return redirect('private_chat_list')


@login_required
def unblock_user(request, user_id):
    blocked_user = get_object_or_404(User, id=user_id)
    Block.objects.filter(blocker=request.user, blocked=blocked_user).delete()
    messages.success(request, f'You have unblocked {blocked_user.username}.')
    return redirect('private_chat_list')



@login_required
def report_user(request, user_id):
    reported_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported = reported_user
            report.save()
            messages.success(request, f'You have reported {reported_user.username}.')
            return redirect('private_chat_list')
    else:
        form = ReportForm()
    return render(request, 'report_user.html', {'form': form, 'reported_user': reported_user})