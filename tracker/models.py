from django.db import models
from django.conf import settings
from core.constants import INCOME, EXPENSE, TRANSACTION_TYPE_CHOICES

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_income = models.BooleanField(default=False) #True - income; False - expense

    def __str__(self):
        return self.name

class Date(models.Model):
    full_date = models.DateField(unique=True)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    weekday = models.CharField(max_length=10)
    quarter = models.IntegerField()

    class Meta:
        ordering = ["full_date"]

    def __str__(self):
        return str(self.full_date)


class Transaction(models.Model):
    # Don’t import User directly, always use settings.AUTH_USER_MODEL.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=False)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES, default=EXPENSE)

    def __str__(self):
        return f"{self.date.full_date} | {self.category} | {self.amount}"
