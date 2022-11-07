"""
Serializers for transaction API.
"""

from rest_framework import serializers
from core.models import Pre_transaction, Transaction

class Pre_transactionSerializer(serializers.ModelSerializer):
    """Serializer for pre_transaction"""

    class Meta:
        model = Pre_transaction
        fields = ['id','description']
        read_only_fields = ['id']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction"""

    class Meta:
        model = Transaction
        fields = ['id',
                'billing_month',
                'date',
                'income',
                'expense',
                'card',
                'currency',
                'supplier',
                'category'
        ]
        read_only_fields = ['id']