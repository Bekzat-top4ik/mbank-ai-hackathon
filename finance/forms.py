from django import forms
from django.db.models import Sum
from .models import Transaction, Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'transaction_type', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Название операции'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Сумма'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-input'
            }),
            'category': forms.Select(attrs={
                'class': 'form-input'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        transaction_type = cleaned_data.get('transaction_type')

        income_total = Transaction.objects.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount'))['total'] or 0

        expense_total = Transaction.objects.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or 0

        balance = income_total - expense_total

        if transaction_type == 'expense' and amount:
            if amount > balance:
                raise forms.ValidationError(
                    f'Недостаточно средств. Текущий баланс: {balance} сом.'
                )

        return cleaned_data

    def save(self, commit=True):
        transaction = super().save(commit=False)

        if not transaction.category:
            title_lower = transaction.title.lower()

            rules = {
                'Продукты': ['магазин', 'супермаркет', 'globus', 'frunze', 'продукты', 'еда'],
                'Транспорт': ['такси', 'yandex', 'яндекс', 'bus', 'маршрутка', 'транспорт'],
                'Кафе': ['кофе', 'cafe', 'кафе', 'burger', 'pizza', 'шаурма'],
                'Зарплата': ['зарплата', 'salary', 'аванс'],
                'Перевод': ['перевод', 'transfer', 'пополнение'],
            }

            for category_name, keywords in rules.items():
                for keyword in keywords:
                    if keyword in title_lower:
                        category = Category.objects.filter(name=category_name).first()
                        if category:
                            transaction.category = category
                            break
                if transaction.category:
                    break

        if commit:
            transaction.save()

        return transaction