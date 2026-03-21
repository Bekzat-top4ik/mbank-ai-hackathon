from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def dashboard(request):
    context = {
        'user_name': request.user.username,
        'balance': 24500,
        'income': 12000,
        'expense': 5300,
        'goal_progress': 68,
        'transactions': [
            {'title': 'Продукты', 'amount': '-850 сом', 'date': '12 мар'},
            {'title': 'Такси', 'amount': '-230 сом', 'date': '11 мар'},
            {'title': 'Пополнение', 'amount': '+5000 сом', 'date': '10 мар'},
            {'title': 'Кофе', 'amount': '-180 сом', 'date': '10 мар'},
        ]
    }
    return render(request, 'dashboard.html', context)