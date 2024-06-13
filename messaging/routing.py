from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:group_id>/', consumers.ChatConsumer.as_asgi()),
]
