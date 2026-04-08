from django.urls import path

from .views import (
    CustomerCreateView,
    CustomerDeleteView,
    CustomerDetailView,
    CustomerListView,
    CustomerUpdateView,
    DashboardView,
    TransactionCreateView,
    TransactionDeleteView,
    TransactionDetailView,
    TransactionListView,
    TransactionUpdateView,
)

app_name = 'wallet'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/new/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/new/', TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
    path('transactions/<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
]
