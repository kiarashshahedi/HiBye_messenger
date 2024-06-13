from django.urls import path
# from rest_framework.routers import DefaultRouter
from .views import groups, group_detail, create_group, join_group, private_chat, accept_request, decline_request

# router = DefaultRouter()
# router.register(r'groups', GroupViewSet)
# router.register(r'messages', MessageViewSet)

urlpatterns = [
    # path('', include(router.urls)), #Api part
    path('groups/', groups, name='groups'),
    path('<int:group_id>/', group_detail, name='group_detail'),
    path('create/', create_group, name='create_group'),
    path('join/<int:group_id>/', join_group, name='join_group'),
    path('private_chat/', private_chat, name='private_chat'),
    path('private_chat/accept/<int:request_id>/', accept_request, name='accept_request'),
    path('private_chat/decline/<int:request_id>/', decline_request, name='decline_request'),
]
