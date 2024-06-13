import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Group, Message
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f'group_{self.group_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        group = await self.get_group(self.group_id)
        user = await self.get_user(data['username'])

        if 'message' in data:
            message = await self.create_message(group, user, data['message'])
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message.content,
                    'username': user.username,
                    'message_type': 'text'
                }
            )
        elif 'image' in data:
            image = await self.create_image_message(group, user, data['image'])
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': image.image.url,
                    'username': user.username,
                    'message_type': 'image'
                }
            )
        elif 'audio' in data:
            audio = await self.create_audio_message(group, user, data['audio'])
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': audio.audio.url,
                    'username': user.username,
                    'message_type': 'audio'
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        message_type = event['message_type']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'message_type': message_type
        }))

    @sync_to_async
    def get_group(self, group_id):
        return Group.objects.get(id=group_id)

    @sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)

    @sync_to_async
    def create_message(self, group, user, content):
        return Message.objects.create(group=group, user=user, content=content)

    @sync_to_async
    def create_image_message(self, group, user, image):
        return Message.objects.create(group=group, user=user, image=image)

    @sync_to_async
    def create_audio_message(self, group, user, audio):
        return Message.objects.create(group=group, user=user, audio=audio)
