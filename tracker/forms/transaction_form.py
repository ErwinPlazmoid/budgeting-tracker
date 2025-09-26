from django import forms
from tracker.models import Transaction
from core.constants import INCOME, EXPENSE

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        t_type = self.cleaned_data.get("type")

        if amount == 0:
            raise forms.ValidationError("Amount cannot be zero.")
        
        if (t_type == INCOME and amount < 0) or (t_type == EXPENSE and amount > 0):
            raise forms.ValidationError("Amount sign does not match transaction type.")

        return amount

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description.stip():
            raise forms.ValidationError("Description cannot be empty.")
        return description