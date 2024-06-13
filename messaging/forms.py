# messaging/forms.py

from django import forms
from .models import Group, Message

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']