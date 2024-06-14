from django import forms
from .models import CoinPackage

class CoinPurchaseForm(forms.Form):
    package = forms.ChoiceField(choices=CoinPackage.COIN_PACKAGES)
