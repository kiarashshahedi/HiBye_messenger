from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from .views import signup, login_view, logout_view

# router = DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('signup/', signup, name='signup'),
    path('login/', login_view , name='login'),
    path('logout/', logout_view, name='logout'),
]
