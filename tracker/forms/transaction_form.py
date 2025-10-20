from django import forms
from tracker.models import Transaction, Date, Category
from core.constants import INCOME, EXPENSE, TRANSACTION_TYPE_CHOICES

class TransactionForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=TRANSACTION_TYPE_CHOICES, 
        widget=forms.RadioSelect
        )

    raw_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
        label="Date",
    )


    class Meta:
        model = Transaction
        fields = ["raw_date", "category", "description", "amount", "type"]
        widgets = {"type": forms.RadioSelect(choices=TRANSACTION_TYPE_CHOICES)}

    def __init__(self, *args, **kwargs):
        # Get user from the view
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter categories by logged-in user
        if self.user is not None:
            self.fields["category"].queryset = Category.objects.filter(user=self.user)
        # Pre-fill date if editing
        if self.instance and self.instance.pk:
            self.fields["raw_date"].initial = self.instance.date.full_date

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

    def save(self, commit=True):
        # get the cleaned date from the HTML input
        raw_date = self.cleaned_data["raw_date"]

        # map to date dimension
        date_obj, _ = Date.objects.get_or_create(
            full_date=raw_date,
            defaults={
                "year": raw_date.year,
                "month": raw_date.month,
                "day": raw_date.day,
                "weekday": raw_date.strftime("%A"),
                "quarter": (raw_date.month - 1) // 3 + 1,
            },
        )

        # replace raw date with date dimension object
        self.instance.date = date_obj
        return super().save(commit=commit)
