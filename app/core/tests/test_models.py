"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@mail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser('test@example.com', 'sample123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is susccessful."""
        user = get_user_model().objects.create_user('test@example.com', 'sample123')

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample title',
            time_minutes=4,
            price=Decimal('5.0'),
            description='Sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful"""
        user = get_user_model().objects.create_user('test@example.com','sample123')
        tag = models.Tag.objects.create(
            user=user,
            name='Tag1'
        )
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating a ingredient is successful."""
        user = get_user_model().objects.create_user('test@example.com','sample123')
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )
        self.assertEqual(str(ingredient), ingredient.name)

# Finazapp tests models

    def test_create_pre_transaction(self):
        """Test creating a pretransaction successful"""
        user = get_user_model().objects.create_user('test@example.com', 'sample123')
        pre_transaction = models.Pre_transaction.objects.create(
            user=user,
            description = 'Te informamos que se ha realizado una compra por $5.987 con Tarjeta de Crédito ****1356 en UBER LAS CONDES CL el 03/11/2022 21:10. Revisa Saldos y Movimientos en App Mi Banco o Banco en Línea.',
        )

        self.assertEqual(str(pre_transaction), pre_transaction.description)

    def test_create_transaction(self):
        """Test creating a transaction successful"""
        user = get_user_model().objects.create_user('test@example.com', 'sample123')
        transaction = models.Transaction.objects.create(
            user=user,
            billing_month = 'July',
            date = '06/11/2022 12:22',
            income = 0,
            expense = 12345,
            card = 'Tarjeta de Crédito ****1356',
            currency = 'CLP',
            supplier = 'UBER LAS CONDES CL',
            category = 'Carrete'
        )

        self.assertEqual(str(transaction), transaction.category)

# new line at the end of the file