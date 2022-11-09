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

    def create(self, validated_data):
        """Create a transaction from pre_transaction"""
        # getting index of substrings
        idx1 = validated_data['description'].index('por ')
        idx2 = validated_data['description'].index(' con')
        res = ''
        # getting elements in between
        for idx in range(idx1 + len('por ') , idx2):
            res = res + validated_data['description'][idx]

        res = res.replace("$","").replace(".","")
        expense = int(res)

        # getting index of substrings
        idx1 = validated_data['description'].index('con ')
        idx2 = validated_data['description'].index(' en')

        res = ''
        # getting elements in between
        for idx in range(idx1 + len('con ') , idx2):
            res = res + validated_data['description'][idx]

        card = res

        dict = {
            'billing_month': 'July',
            'date': '06/11/2022 17:28',
            'income': None,
            'expense': expense,
            'card': card,
            'currency': 'CLP',
            'supplier': 'Uber',
            'category': 'Transporte'
        }
        transaction = Transaction.objects.create(**dict)

        return transaction


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

