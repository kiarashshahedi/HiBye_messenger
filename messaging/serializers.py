from rest_framework import serializers
from .models import Group, Message

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'created_by', 'members')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'group', 'sender', 'content', 'timestamp')
