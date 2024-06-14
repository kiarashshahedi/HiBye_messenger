from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='member_groups')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    voice = models.FileField(upload_to='voices/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class PrivateChatRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver} ({self.status})"
    
    
    
class PrivateChat(models.Model):
    participants = models.ManyToManyField(User, related_name='private_chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ", ".join(participant.username for participant in self.participants.all())

class PrivateMessage(models.Model):
    chat = models.ForeignKey(PrivateChat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='private_messages_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='private_messages_received', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='private_images/', blank=True, null=True)
    voice = models.FileField(upload_to='private_voices/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content}"
    
    
    
class Block(models.Model):
    blocker = models.ForeignKey(User, related_name='blocker', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='blocked', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"
    
    
class Report(models.Model):
    reporter = models.ForeignKey(User, related_name='reporter', on_delete=models.CASCADE)
    reported = models.ForeignKey(User, related_name='reported', on_delete=models.CASCADE)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reporter.username} reported {self.reported.username} - {self.reason[:20]}"