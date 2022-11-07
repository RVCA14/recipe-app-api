"""
Views for the transaction API.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Pre_transaction, Transaction
from transaction import serializers

class Pre_transactionViewSet(viewsets.ModelViewSet):
    """View for manage pretansaction API"""
    serializer_class = serializers.Pre_transactionSerializer
    queryset = Pre_transaction.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

class TransactionViewSet(viewsets.ModelViewSet):
    """View for manage pretansaction API"""
    serializer_class = serializers.TransactionSerializer
    queryset = Transaction.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')