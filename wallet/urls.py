from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, transactions, purchase_coins, payment_callback

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', transactions, name='transactions'),  # Add this line
    path('purchase_coins/', purchase_coins, name='purchase_coins'),
    path('payment/callback/', payment_callback, name='payment_callback'),

]
