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
        'card': 'Débito',
        'currency': 'CLP',
        'supplier': 'UBER',
        'category': 'Transporte'

    }
    defaults.update(params)

    transaction = Transaction.objects.create(user=user, **defaults)
    return transaction

TRANSACTIONS_URL = reverse('transaction:transaction-list')
PRE_TRANSACTIONS_URL = reverse('transaction:pre_transaction-list')

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

    def test_retrieve_transaction(self):
        """Test retrieving a list of recipes."""
        create_transaction(user=self.user)
        create_transaction(user=self.user)

        res = self.client.get(TRANSACTIONS_URL)

        transactions = Transaction.objects.all().order_by('-id')
        serializer = TransactionSerializer(transactions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_transaction_list_limited_to_user(self):
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

    def test_creation_transaction(self):
        """Test creating a transaction"""
        payload = {
            'billing_month': 'July',
            'date': '06/11/2022 17:28',
            'expense': 3512,
            'card': 'Débito',
            'currency': 'CLP',
            'supplier': 'UBER',
            'category': 'Transporte'
        }
        res = self.client.post(TRANSACTIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        transaction = Transaction.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(transaction, k), v)
        self.assertEqual(transaction.user, self.user)


    def test_creation_pre_transaction(self):
        """Test creating a pre-transaction"""
        payload = {
            'description': 'Te informamos que se ha realizado una compra por $5.987 con Tarjeta de Crédito ****1356 en UBER LAS CONDES CL el 03/11/2022 21:10. Revisa Saldos y Movimientos en App Mi Banco o Banco en Línea.',
        }
        res = self.client.post(PRE_TRANSACTIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        pre_transaction = Pre_transaction.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(pre_transaction, k), v)
        self.assertEqual(pre_transaction.user, self.user)

    def test_creation_transaction_from_pre_transaction(self):
        """Test creating a transaction from a pre-transaction"""
        payload = {
            'description': 'Te informamos que se ha realizado una compra por $5.987 con Tarjeta de Crédito ****1356 en UBER LAS CONDES CL el 03/11/2022 21:10. Revisa Saldos y Movimientos en App Mi Banco o Banco en Línea.',
        }
        res = self.client.post(PRE_TRANSACTIONS_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        payload_transform = {
            'billing_month': 'July',
            'date': '06/11/2022 17:28',
            'expense': 5987,
            'card': 'Débito',
            'currency': 'CLP',
            'supplier': 'UBER',
            'category': 'Transporte'

        }
        transaction = Transaction.objects.get(id=res.data['id'])
        for k, v in payload_transform.items():
            self.assertEqual(getattr(transaction, k), v)
        self.assertEqual(transaction.user, self.user)
