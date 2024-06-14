from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

class CoinPackage(models.Model):
    COIN_PACKAGES = [
        (50, '50 coins for 100,000 tomans'),
        (100, '100 coins for 100,000 tomans'),
        (200, '200 coins for 150,000 tomans'),
    ]

    coins = models.IntegerField(choices=COIN_PACKAGES)
    price = models.IntegerField()

class CoinTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coins = models.IntegerField()
    price = models.IntegerField()
    successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)