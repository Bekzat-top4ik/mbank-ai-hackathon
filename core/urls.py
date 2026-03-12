from django.urls import path
from .views import home, dashboard, add_transaction, transactions_list, budget_warning_api

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-transaction/', add_transaction, name='add_transaction'),
    path('transactions/', transactions_list, name='transactions'),
    path('api/budget-warning/', budget_warning_api, name='budget_warning_api'),
]