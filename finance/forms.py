from django import forms
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