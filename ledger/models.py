from django.db import models
import random

class BalanceArticle(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BalanceGroup(models.Model):
    name = models.CharField(max_length=255)
    article = models.ForeignKey(BalanceArticle, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return self.name

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('active', 'Актив'),
        ('passive', 'Пассив'),
        ('active_passive', 'Активно-пассивный'),
    ]

    number = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    group = models.ForeignKey(BalanceGroup, on_delete=models.CASCADE, related_name='accounts')

    def save(self, *args, **kwargs):
        if not self.number:
            while True:
                num = ''.join(str(random.randint(0, 9)) for _ in range(10))
                if not Account.objects.filter(number=num).exists():
                    self.number = num
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    debit_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='debit_transactions')
    credit_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='credit_transactions')

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d')}, {self.amount}"
