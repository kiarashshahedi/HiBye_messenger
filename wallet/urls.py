from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, transactions

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', transactions, name='transactions'),  # Add this line

]
