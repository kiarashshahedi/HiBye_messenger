import requests

from rest_framework import viewsets
from django.views.generic import View
from .forms import CoinPurchaseForm
from .models import Transaction, CoinTransaction, CoinPackage
from .serializers import TransactionSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def transactions(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transactions.html', {'transactions': user_transactions})

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer



class PurchaseCoinsView(View):
    def get(self, request):
        return render(request, 'purchase_coins.html')

    def post(self, request):
        amount = int(request.POST['amount'])
        request.user.coins += amount
        request.user.save()
        return redirect('index')
    
    
@login_required
def purchase_coins(request):
    if request.method == 'POST':
        form = CoinPurchaseForm(request.POST)
        if form.is_valid():
            package = form.cleaned_data['package']
            coins, price = CoinPackage.COIN_PACKAGES[int(package)]
            transaction = CoinTransaction.objects.create(
                user=request.user, coins=coins, price=price
            )

            # Dummy payment gateway integration
            payment_data = {
                'amount': price,
                'user_id': request.user.id,
                'transaction_id': transaction.id,
                'callback_url': request.build_absolute_uri('/payment/callback/')
            }
            response = requests.post('https://payment-gateway.com/api/pay', data=payment_data)
            payment_url = response.json().get('payment_url')
            return redirect(payment_url)
    else:
        form = CoinPurchaseForm()
    return render(request, 'purchase_coins.html', {'form': form})

@login_required
def payment_callback(request):
    transaction_id = request.GET.get('transaction_id')
    payment_status = request.GET.get('status')  # This will be according to your payment gateway's response

    transaction = get_object_or_404(CoinTransaction, id=transaction_id)
    if payment_status == 'success':
        transaction.successful = True
        transaction.user.profile.coins += transaction.coins
        transaction.user.profile.save()
        transaction.save()
        return render(request, 'payment_success.html', {'transaction': transaction})
    else:
        return render(request, 'payment_failure.html', {'transaction': transaction})