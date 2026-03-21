from django.contrib.auth.models import User
from django.db import models

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)


    def percentage(self):
        if self.target_amount == 0:
            return 0
        return round((self.current_amount / self.target_amount) * 100, 1)

    def __str__(self):
        return self.title