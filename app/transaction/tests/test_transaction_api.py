"""
Tests for Transaction APIs
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Pre_transaction, Transaction
from transaction.serializers import (Pre_transactionSerializer, TransactionSerializer)


def create_transaction(user, **params):
    """Create and return a sample pre_transaction."""
    defaults = {
        'billing_month': 'October',
        'date': '06/11/2022 17:28',
        'expense': 3512,
        'income': 0,
        'card': 'Débito',
        'currency': 'CLP',
        'supplier': 'UBER',
        'category': 'Transporte'

    }
    defaults.update(params)

    transaction = Transaction.objects.create(user=user, **defaults)
    return transaction

TRANSACTIONS_URL = reverse('transaction:transaction-list')

class PublicRecipeAPITests(TestCase):
    """Test unauthenticate API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(TRANSACTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticate API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'test1234'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_transaction(user=self.user)
        create_transaction(user=self.user)

        res = self.client.get(TRANSACTIONS_URL)

        transactions = Transaction.objects.all().order_by('-id')
        serializer = TransactionSerializer(transactions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited by the authenticated user"""
        other_user = get_user_model().objects.create_user(
            'another-user@example.com',
            "test1234"
        )
        create_transaction(user=other_user)
        create_transaction(user=self.user)

        transactions = Transaction.objects.filter(user=self.user)
        serializer= TransactionSerializer(transactions, many=True)

        res = self.client.get(TRANSACTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

