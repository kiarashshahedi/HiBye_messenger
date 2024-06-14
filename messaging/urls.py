from django.urls import path
# from rest_framework.routers import DefaultRouter
from .views import (
    groups, group_detail, create_group, join_group, leave_group,
    private_chat_list, start_private_chat, private_chat_detail, 
    send_private_chat_request, handle_private_chat_request, 
    private_chat_requests, block_user, report_user, unblock_user)

# router = DefaultRouter()
# router.register(r'groups', GroupViewSet)
# router.register(r'messages', MessageViewSet)

urlpatterns = [
    # path('', include(router.urls)), #Api part
    path('groups/', groups, name='groups'),
    path('<int:group_id>/', group_detail, name='group_detail'),
    path('create/', create_group, name='create_group'),
    path('join/<int:group_id>/', join_group, name='join_group'),
    path('leave_group/<int:group_id>/', leave_group, name='leave_group'),

    
    # private chats links
    path('private_chat_list/', private_chat_list, name='private_chat_list'),
    path('start_private_chat/<int:user_id>/', start_private_chat, name='start_private_chat'),
    path('private_chat/<int:chat_id>/', private_chat_detail, name='private_chat_detail'),
    path('send_private_chat_request/', send_private_chat_request, name='send_private_chat_request'),
    path('private_chat_requests/', private_chat_requests, name='private_chat_requests'),
    path('handle_private_chat_request/<int:request_id>/<str:action>/', handle_private_chat_request, name='handle_private_chat_request'),

    # Blocking and reporting urls
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('unblock/<int:user_id>/', unblock_user, name='unblock_user'),

    path('report_user/<int:user_id>/', report_user, name='report_user'),
]


