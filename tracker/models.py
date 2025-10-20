from django.db import models
from django.conf import settings
from core.constants import INCOME, EXPENSE, TRANSACTION_TYPE_CHOICES

class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="categories"
        )
    name = models.CharField(max_length=50)
    is_income = models.BooleanField(default=False) #True - income; False - expense

    class Meta:
        # 🔹 Unique per user instead of globally unique
        unique_together = ("user", "name")
        ordering = ["name"]

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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="transactions"
        )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name="transactions"
        )
    date = models.ForeignKey(
        Date, 
        on_delete=models.CASCADE
        )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2
        )
    description = models.TextField(blank=False)
    type = models.CharField(
        max_length=7, 
        choices=TRANSACTION_TYPE_CHOICES, 
        default=EXPENSE
        )

    class Meta:
        ordering = ["-date__full_date"]

    def __str__(self):
        return f"{self.date.full_date} | {self.get_type_display()} | {self.category} | {self.amount}"

    def signed_amount(self):
        if self.type == "income":
            return f"+{abs(self.amount)}"
        return f"-{abs(self.amount)}"
