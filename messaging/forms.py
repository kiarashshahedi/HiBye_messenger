# messaging/forms.py

from django import forms
from .models import Group, Message, PrivateMessage

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'image', 'voice']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1}),
        }
        
        
class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content', 'image', 'voice']