from django import forms
from tracker.models import Transaction
from core.constants import INCOME, EXPENSE, TRANSACTION_TYPE_CHOICES

class TransactionForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=TRANSACTION_TYPE_CHOICES, 
        widget=forms.RadioSelect
        )

    class Meta:
        model = Transaction
        fields = ["date", "category", "description", "amount", "type"]
        widgets = {"type": forms.RadioSelect(choices=TRANSACTION_TYPE_CHOICES)}

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        t_type = self.cleaned_data.get("type")

        if amount == 0:
            raise forms.ValidationError("Amount cannot be zero.")

        # Auto-normalize sign
        if t_type == INCOME:
            return abs(amount)  # always positive

        elif t_type == EXPENSE:
            return -abs(amount)  # always negative

        return amount

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description.strip():
            raise forms.ValidationError("Description cannot be empty.")
        return description
