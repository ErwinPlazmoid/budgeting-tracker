from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Transaction

# Home
class HomeView(TemplateView):
    template_name = "tracker/home.html"


# Transactions
class TransactionListView(ListView):
    model = Transaction
    template_name = "tracker/transactions/list.html"
    context_object_name = "transactions"

    def get_querry_set(self):
        # For now: return ALL transactions
        # Later: filter by self.request.user
        return Transaction.objects.all().order_by("-date__full_date")

class TransactionCreateView(CreateView):
    model = Transaction
    template_name = "tracker/transactions/add.html"
    fields = ["date", "category", "description", "amount"]
    success_url = reverse_lazy("transaction-list")

    def form_valid(self, form):
        # Later, tie to logged-in user.
        # For now: just pick the first user in DB.
        form.instance.user_id = 1
        return super().form_valid(form)

class TransactionUpdateView(UpdateView):
    model = Transaction
    template_name = "tracker/transactions/edit.html"
    fields = ["date", "category", "description", "amount"]
    success_url = reverse_lazy("transaction-list")

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = "tracker/transactions/delete.html"
    success_url = reverse_lazy("transaction-list")


# Categories
class CategoryListView(TemplateView):
    template_name = "tracker/categories/list.html"

class CategoryCreateView(TemplateView):
    template_name = "tracker/categories/add.html"

class CategoryUpdateView(TemplateView):
    template_name = "tracker/categories/edit.html"

class CategoryDeleteView(TemplateView):
    template_name = "tracker/categories/delete.html"


# Analytics
class AnalyticsHomeView(TemplateView):
    template_name = "tracker/analytics/home.html"

class AnalyticsSummaryView(TemplateView):
    template_name = "tracker/analytics/summary.html"

class AnalyticsMonthlyView(TemplateView):
    template_name = "tracker/analytics/monthly.html"

class AnalyticsCategoriesView(TemplateView):
    template_name = "tracker/analytics/categories.html"
