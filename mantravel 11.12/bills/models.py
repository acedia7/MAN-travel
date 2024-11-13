from django.db import models

class Budget(models.Model):
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('transport', '交通'),
        ('accommodation', '住宿'),
        ('food', '美食'),
        ('attraction', '景点'),
        ('shopping', '购物'),
        ('activity', '活动'),
        ('other', '其他'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category}: ¥{self.amount}"