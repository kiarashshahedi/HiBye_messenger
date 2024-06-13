from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Group, Message, PrivateChatRequest
from .serializers import GroupSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from wallet.models import Transaction
from django.contrib.auth.decorators import login_required


User = get_user_model()

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        group = self.get_object()
        user = request.user
        if user.coins > 0:
            group.members.add(user)
            user.coins -= 1
            user.save()
            Transaction.objects.create(user=user, amount=-1, description='Joined group')
            return Response({'status': 'joined group'})
        return Response({'status': 'insufficient coins'}, status=400)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# page for showing all groups 
@login_required
def groups(request):
    groups = Group.objects.all()
    return render(request, 'groups.html', {'groups': groups})

# page for each group when join
@login_required
def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    return render(request, 'group_detail.html', {'group': group})

# Create group
@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        if name:
            group = Group.objects.create(name=name, description=description, created_by=request.user)
            group.members.add(request.user)  # Add the creator to the group members
            return redirect('groups')
        else:
            return render(request, 'create_group.html', {'error': 'Name is required.'})
    return render(request, 'create_group.html')


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