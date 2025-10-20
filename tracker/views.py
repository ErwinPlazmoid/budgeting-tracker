from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Transaction, Category
from django.db.models import Sum, Q
from tracker.forms.transaction_form import TransactionForm
from .mixins import MessageDeleteMixin, MessageCreateUpdateMixin, PaginateByMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Home
class HomeView(TemplateView):
    template_name = "tracker/home.html"


# Transactions
class TransactionListView(LoginRequiredMixin, PaginateByMixin, ListView):
    model = Transaction
    template_name = "tracker/transactions/list.html"
    context_object_name = "transactions"
    paginate_by = 10
    login_url = "login"  
    redirect_field_name = "next"

    def get_queryset(self):
        # Show only transactions belonging to the current user
        qs = Transaction.objects.filter(user=self.request.user)

        # Sorting
        sort = self.request.GET.get("sort")
        allowed_sorts = {
            "date": "date__full_date",
            "-date": "-date__full_date",
            "amount": "amount",
            "-amount": "-amount"
        }
        qs = qs.order_by(allowed_sorts.get(sort, "-date__full_date"))

        # Filter by category
        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)

        # Filter by date
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date:
            qs = qs.filter(date__full_date__gte=start_date)
        if end_date:
            qs = qs.filter(date__full_date__lte=end_date)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Categories only for this user
        context["categories"] = Category.objects.filter(user=self.request.user)

        # Keep current filters/sort in querystring (except page)
        params = self.request.GET.copy()

        # For pagination: keep filters & sort, drop page
        params.pop("page", None)
        context["querystring"] = params.urlencode()

        # For sorting links: keep filters, drop page and old sort
        params_no_sort = params.copy()
        params_no_sort.pop("sort", None)
        context["querystring_no_sort"] = params_no_sort.urlencode()

        return context


class TransactionCreateView(LoginRequiredMixin, MessageCreateUpdateMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "tracker/transactions/add.html"
    success_url = reverse_lazy("transaction-list")
    success_message = "✅ Transaction created successfully!"
    login_url = "login"
    redirect_field_name = "next"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass logged-in user to form
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Assign logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, MessageCreateUpdateMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "tracker/transactions/edit.html"
    success_url = reverse_lazy("transaction-list")
    success_message = "✏️ Transaction updated successfully!"
    login_url = "login"
    redirect_field_name = "next"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass logged-in user to form
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        # Restrict editing to user's own transactions
        return Transaction.objects.filter(user=self.request.user)


class TransactionDeleteView(LoginRequiredMixin, MessageDeleteMixin, DeleteView):
    model = Transaction
    template_name = "tracker/transactions/delete.html"
    success_url = reverse_lazy("transaction-list")
    success_message = "🗑 Transaction deleted."
    login_url = "login"
    redirect_field_name = "next"

    def get_queryset(self):
        # Restrict deletion to user's own transactions
        return Transaction.objects.filter(user=self.request.user)


# Categories
class CategoryListView(LoginRequiredMixin, PaginateByMixin, ListView):
    model = Category
    template_name = "tracker/categories/list.html"
    context_object_name = "categories"
    paginate_by = 10
    login_url = "login"
    redirect_field_name = "next"

    def get_queryset(self):
        # Filter only categories created by the logged-in user
        return Category.objects.filter(user=self.request.user).order_by("name")


class CategoryCreateView(LoginRequiredMixin, MessageCreateUpdateMixin, CreateView):
    model = Category
    template_name = "tracker/categories/add.html"
    fields = ["name"]
    success_url = reverse_lazy("category-list")
    success_message = "✅ Category created successfully!"
    login_url = "login"
    redirect_field_name = "next"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, MessageCreateUpdateMixin, UpdateView):
    model = Category
    template_name = "tracker/categories/edit.html"
    fields = ["name"]
    success_url = reverse_lazy("category-list")
    success_message = "✏️ Category updated successfully!"
    login_url = "login"
    redirect_field_name = "next"

    def get_queryset(self):
        # Prevent editing categories that belong to another user
        return Category.objects.filter(user=self.request.user)


class CategoryDeleteView(LoginRequiredMixin, MessageDeleteMixin, DeleteView):
    model = Category
    template_name = "tracker/categories/delete.html"
    success_url = reverse_lazy("category-list")
    success_message = "🗑 Category deleted."
    login_url = "login"
    redirect_field_name = "next"

    def get_queryset(self):
        # Prevent deleting categories that belong to another user
        return Category.objects.filter(user=self.request.user)


# Analytics
class AnalyticsHomeView(TemplateView):
    template_name = "tracker/analytics/home.html"

class AnalyticsSummaryView(TemplateView):
    template_name = "tracker/analytics/summary.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Agg totals
        totals = Transaction.objects.aggregate(
            total_income = Sum("amount", filter = Q(amount__gt=0)),
            total_expenses = Sum("amount", filter = Q(amount__lt=0)),
        )

        income = totals["total_income"] or 0
        expenses = totals["total_expenses"] or 0
        expenses = abs(expenses)
        balance = income - expenses

        context.update({
            "income":income,
            "expenses":expenses,
            "balance":balance
        })
        return context

class AnalyticsMonthlyView(TemplateView):
    template_name = "tracker/analytics/monthly.html"

class AnalyticsCategoriesView(TemplateView):
    template_name = "tracker/analytics/categories.html"
