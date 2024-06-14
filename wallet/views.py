from rest_framework import viewsets
from django.views.generic import View

from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import render, redirect
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