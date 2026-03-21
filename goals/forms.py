from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'target_amount', 'current_amount', 'deadline']
        labels = {
            'title': 'Название цели',
            'target_amount': 'Сумма накопления',
            'current_amount': 'Уже накоплено',
            'deadline': 'Дедлайн',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Например: Купить MacBook',
                'style': 'width:100%; padding:8px; border-radius:6px; border:1px solid #ccc;'
            }),
            'target_amount': forms.NumberInput(attrs={
                'placeholder': 'Например: 120000',
                'style': 'width:100%; padding:8px; border-radius:6px; border:1px solid #ccc;'
            }),
            'current_amount': forms.NumberInput(attrs={
                'placeholder': 'Например: 30000',
                'style': 'width:100%; padding:8px; border-radius:6px; border:1px solid #ccc;'
            }),
            'deadline': forms.DateInput(format='%d.%m.%Y', attrs={
                'placeholder': '28.05.2026',
                'style': 'width:100%; padding:8px; border-radius:6px; border:1px solid #ccc;'
            }),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['deadline'].input_formats = ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y']