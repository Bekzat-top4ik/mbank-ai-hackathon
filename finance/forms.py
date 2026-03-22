from decimal import Decimal
from django import forms
from django.db.models import Sum
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'transaction_type', 'category']
        labels = {
            'title': 'Название',
            'amount': 'Сумма',
            'transaction_type': 'Тип операции',
            'category': 'Категория',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Например: Кофе'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите сумму'
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

        if amount and transaction_type == 'expense':
            income_total = Transaction.objects.filter(
                transaction_type='income'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

            expense_total = Transaction.objects.filter(
                transaction_type='expense'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

            balance = income_total - expense_total

            if amount > balance:
                raise forms.ValidationError(
                    f'Недостаточно средств. Текущий баланс: {balance} сом.'
                )

        return cleaned_data