# messaging/forms.py

from django import forms
from .models import Group, Message, PrivateMessage, Report

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
        
        
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }