from django.urls import path
from . import views
urlpatterns = [
    path('', views.goals_list, name='goals_list'),
    path('add/', views.add_goal, name='add_goal'),
    path('edit/<int:id>/', views.edit_goal, name='edit_goal'),
    path('delete/<int:id>/', views.delete_goal, name='delete_goal'),
    path('add-amount/<int:id>/', views.add_amount, name='add_amount'),
]