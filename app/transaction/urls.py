"""
URL mappings for the transaction app.
"""
from django.urls import (path, include)

from rest_framework.routers import DefaultRouter

from transaction import views

router = DefaultRouter()
router.register('pre_transactions', views.Pre_transactionViewSet)
router.register('transactions', views.TransactionViewSet)

app_name = 'transaction'

urlpatterns = [
    path('', include(router.urls))
]