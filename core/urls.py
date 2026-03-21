from django.urls import path
<<<<<<< HEAD
from .views import home, dashboard, add_transaction, transactions_list, budget_warning_api
=======
from .views import home, dashboard
>>>>>>> e45c40c9bb56f3ceba5d01ca611cde93739d173e

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
<<<<<<< HEAD
    path('add-transaction/', add_transaction, name='add_transaction'),
    path('transactions/', transactions_list, name='transactions'),
    path('api/budget-warning/', budget_warning_api, name='budget_warning_api'),
=======
>>>>>>> e45c40c9bb56f3ceba5d01ca611cde93739d173e
]