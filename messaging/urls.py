from django.urls import path
# from rest_framework.routers import DefaultRouter
from .views import groups, group_detail, create_group, join_group, accept_request, decline_request, private_chat_detail, start_private_chat, private_chat_list, send_private_chat_request, handle_private_chat_request, private_chat_requests, private_chats

# router = DefaultRouter()
# router.register(r'groups', GroupViewSet)
# router.register(r'messages', MessageViewSet)

urlpatterns = [
    # path('', include(router.urls)), #Api part
    path('groups/', groups, name='groups'),
    path('<int:group_id>/', group_detail, name='group_detail'),
    path('create/', create_group, name='create_group'),
    path('join/<int:group_id>/', join_group, name='join_group'),
    
    # private chats links
    path('private_chat_list/', private_chat_list, name='private_chat_list'),
    path('start_private_chat/<int:user_id>/', start_private_chat, name='start_private_chat'),
    path('private_chat/<int:chat_id>/', private_chat_detail, name='private_chat_detail'),
    path('send_private_chat_request/<int:user_id>/', send_private_chat_request, name='send_private_chat_request'),
    path('handle_private_chat_request/<int:request_id>/<str:action>/', handle_private_chat_request, name='handle_private_chat_request'),
    path('private_chat_requests/', private_chat_requests, name='private_chat_requests'),
    path('private_chats/', private_chats, name='private_chat'),
    path('accept_request/<int:request_id>/', accept_request, name='accept_request'),
    path('decline_request/<int:request_id>/', decline_request, name='decline_request'),
]
