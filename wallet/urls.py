from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, transactions, PurchaseCoinsView

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', transactions, name='transactions'),  # Add this line
    path('purchase_coins/', PurchaseCoinsView.as_view(), name='purchase_coins'),


]
