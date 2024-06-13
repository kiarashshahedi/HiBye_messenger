from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def transactions(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transactions.html', {'transactions': user_transactions})

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
