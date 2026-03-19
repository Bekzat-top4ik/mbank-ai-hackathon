from django.shortcuts import render, redirect
from django.db.models import Sum
from finance.models import Transaction
from finance.forms import TransactionForm
from datetime import date, datetime, timedelta
import calendar
from django.http import JsonResponse



def home(request):
    return render(request, 'home.html')


def budget_warning_api(request):
    income_total = Transaction.objects.filter(
        transaction_type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    expense_total = Transaction.objects.filter(
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    balance = income_total - expense_total

    today = date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_passed = today.day
    days_left = days_in_month - today.day

    avg_daily_expense = 0
    predicted_expense = 0
    predicted_balance = balance

    if days_passed > 0:
        avg_daily_expense = expense_total / days_passed
        predicted_expense = avg_daily_expense * days_left
        predicted_balance = balance - predicted_expense

    warning_message = None

    if predicted_balance < 0:
        warning_message = (
            "Внимание: если расходы продолжатся в таком темпе, "
            "к концу месяца баланс может уйти в минус."
        )
    elif avg_daily_expense > 0 and predicted_expense > balance:
        warning_message = (
            "Предупреждение: текущий темп расходов слишком высокий. "
            "Рекомендуется сократить траты."
        )
    elif expense_total > income_total and income_total > 0:
        warning_message = (
            "Расходы уже превышают доходы. Стоит пересмотреть бюджет."
        )

    return JsonResponse({
        'has_warning': bool(warning_message),
        'warning_message': warning_message,
    })

def dashboard(request):
    today = date.today()

    month_transactions = Transaction.objects.filter(
        created_at__year=today.year,
        created_at__month=today.month
    )

    transactions = month_transactions.order_by('-created_at')[:5]

    income_total = month_transactions.filter(
        transaction_type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    expense_total = month_transactions.filter(
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    balance = income_total - expense_total

    category_stats = (
        month_transactions
        .filter(transaction_type='expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_passed = today.day
    days_left = days_in_month - today.day

    avg_daily_expense = 0
    predicted_expense = 0
    predicted_balance = balance

    if days_passed > 0:
        avg_daily_expense = expense_total / days_passed
        predicted_expense = avg_daily_expense * days_left
        predicted_balance = balance - predicted_expense

    top_category = category_stats[0] if category_stats else None
    ai_tip = "Пока недостаточно данных для совета."

    if top_category:
        category_name = top_category['category__name'] or "Без категории"
        ai_tip = (
            f"Больше всего расходов уходит на категорию "
            f"«{category_name}». Попробуй сократить траты в этой категории."
        )

    category_labels = []
    category_totals = []

    for stat in category_stats:
        category_labels.append(stat['category__name'] or 'Без категории')
        category_totals.append(float(stat['total']))

    warning_message = None
    notify_title = request.session.pop('notify_title', None)
    notify_message = request.session.pop('notify_message', None)

    context = {
        'user_name': 'Bekzat',
        'balance': balance,
        'income': income_total,
        'expense': expense_total,
        'transactions': transactions,
        'category_stats': category_stats,
        'avg_daily_expense': round(avg_daily_expense, 2),
        'predicted_expense': round(predicted_expense, 2),
        'predicted_balance': round(predicted_balance, 2),
        'days_left': days_left,
        'ai_tip': ai_tip,
        'category_labels': category_labels,
        'category_totals': category_totals,
        'warning_message': warning_message,
        'notify_title': notify_title,
        'notify_message': notify_message,
        'current_month': today.strftime('%B'),
    }

    return render(request, 'dashboard.html', context)
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()

            request.session['notify_title'] = 'Новая операция'
            request.session['notify_message'] = f'Операция "{transaction.title}" на сумму {transaction.amount} сом успешно добавлена.'

            if transaction.transaction_type == 'expense' and transaction.amount >= 3000:
                request.session['notify_title'] = 'Крупный расход'
                request.session['notify_message'] = f'Обнаружен крупный расход: {transaction.amount} сом.'

            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'add_transaction.html', {'form': form})

def transactions_list(request):
    transactions = Transaction.objects.order_by('-created_at')
    return render(request, 'transactions.html', {'transactions': transactions})
