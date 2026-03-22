from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, blank=True, null=True)  # например: 🍔 🚗 💳

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]

    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.amount})"