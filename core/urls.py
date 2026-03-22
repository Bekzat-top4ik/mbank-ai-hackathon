from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/transactions/', views.transactions_list, name='transactions'),
    path('dashboard/add_transaction/', views.add_transaction, name='add_transaction'),

    path('api/budget-warning/', views.budget_warning_api, name='budget_warning_api'),
]