from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Message, PrivateChatRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import GroupForm, MessageForm

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
    if request.user not in group.members.all():
        return redirect('index')  # Redirect if the user is not a member of the group

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.group = group
            message.user = request.user
            message.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = MessageForm()

    messages = group.messages.all().order_by('timestamp')
    members = group.members.all()
    return render(request, 'group_detail.html', {'group': group, 'form': form, 'messages': messages, 'members': members})

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

            return redirect('groups') 
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})


# join a group
@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.add(request.user)
    return redirect('group_detail', group_id=group_id)

# private chat page
@login_required
def private_chat(request):
    received_requests = PrivateChatRequest.objects.filter(receiver=request.user, status='pending')
    return render(request, 'private_chat.html', {'requests': received_requests})

# private chat accept
@login_required
def accept_request(request, request_id):
    chat_request = get_object_or_404(PrivateChatRequest, id=request_id, receiver=request.user)
    chat_request.status = 'accepted'
    chat_request.save()
    return redirect('private_chat')


# private chat decline
@login_required
def decline_request(request, request_id):
    chat_request = get_object_or_404(PrivateChatRequest, id=request_id, receiver=request.user)
    chat_request.status = 'declined'
    chat_request.save()
    return redirect('private_chat')