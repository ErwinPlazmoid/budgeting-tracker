from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Transaction, Category
from django.db.models import Sum, Q
from tracker.forms.transaction_form import TransactionForm

# Home
class HomeView(TemplateView):
    template_name = "tracker/home.html"


# Transactions
class TransactionListView(ListView):
    model = Transaction
    template_name = "tracker/transactions/list.html"
    context_object_name = "transactions"
    ordering = ['-date__full_date']
    paginate_by = 10

    def get_querry_set(self):
        # For now: return ALL transactions
        # Later: filter by self.request.user
        return Transaction.objects.all().order_by("-date__full_date")

    def get_paginate_by(self, queryset):
        # Get "page_size" from query params (?page_size=20)
        page_size = self.request.GET.get("page_size")
        if page_size in ["10", "20", "50", "100"]:
            return int(page_size)
        return 10  # default

class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "tracker/transactions/add.html"
    success_url = reverse_lazy("transaction-list")

    def form_valid(self, form):
        # Later, tie to logged-in user.
        # For now: just pick the first user in DB.
        form.instance.user_id = 1
        return super().form_valid(form)

class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "tracker/transactions/edit.html"
    success_url = reverse_lazy("transaction-list")

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = "tracker/transactions/delete.html"
    success_url = reverse_lazy("transaction-list")


# Categories
class CategoryListView(ListView):
    model = Category
    template_name = "tracker/categories/list.html"
    context_object_name = "categories"
    ordering = ["name"]
    paginate_by = 10

    def get_queryset(self):
        # For now: return ALL categories
        # Later: filter by self.request.user
        return Category.objects.all().order_by("name")


class CategoryCreateView(CreateView):
    model = Category
    template_name = "tracker/categories/add.html"
    fields = ["name"]
    success_url = reverse_lazy("category-list")

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = "tracker/categories/edit.html"
    fields = ["name"]
    success_url = reverse_lazy("category-list")

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "tracker/categories/delete.html"
    success_url = reverse_lazy("category-list")


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
