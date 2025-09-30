from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Transaction, Category
from django.db.models import Sum, Q
from tracker.forms.transaction_form import TransactionForm
from .mixins import MessageDeleteMixin, MessageCreateUpdateMixin, PaginateByMixin

# Home
class HomeView(TemplateView):
    template_name = "tracker/home.html"


# Transactions
class TransactionListView(PaginateByMixin, ListView):
    model = Transaction
    template_name = "tracker/transactions/list.html"
    context_object_name = "transactions"
    paginate_by = 10

    def get_queryset(self):
        qs = Transaction.objects.all()

        # Sorting
        sort = self.request.GET.get("sort")
        allowed_sorts = {
            "date": "date__full_date",
            "-date": "-date__full_date",
            "amount": "amount",
            "-amount": "-amount"
        }
        if sort in allowed_sorts:
            qs = qs.order_by(allowed_sorts[sort])
        else:
            qs = qs.order_by("-date__full_date")

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
        context["categories"] = Category.objects.all()

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


class TransactionCreateView(MessageCreateUpdateMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "tracker/transactions/add.html"
    success_url = reverse_lazy("transaction-list")
    success_message = "✅ Transaction created successfully!"

    def form_valid(self, form):
        # Later, tie to logged-in user.
        # For now: just pick the first user in DB.
        form.instance.user_id = 1
        return super().form_valid(form)


class TransactionUpdateView(MessageCreateUpdateMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "tracker/transactions/edit.html"
    success_url = reverse_lazy("transaction-list")
    success_message = "✏️ Transaction updated successfully!"

    def form_valid(self, form):
        return super().form_valid(form)


class TransactionDeleteView(MessageDeleteMixin, DeleteView):
    model = Transaction
    template_name = "tracker/transactions/delete.html"
    success_url = reverse_lazy("transaction-list")
    success_message = "🗑 Transaction deleted."


# Categories
class CategoryListView(PaginateByMixin, ListView):
    model = Category
    template_name = "tracker/categories/list.html"
    context_object_name = "categories"
    paginate_by = 10

    def get_queryset(self):
        # For now: return ALL categories
        # Later: filter by self.request.user
        return Category.objects.all().order_by("name")


class CategoryCreateView(MessageCreateUpdateMixin, CreateView):
    model = Category
    template_name = "tracker/categories/add.html"
    fields = ["name"]
    success_url = reverse_lazy("category-list")
    success_message = "✅ Category created successfully!"


class CategoryUpdateView(MessageCreateUpdateMixin, UpdateView):
    model = Category
    template_name = "tracker/categories/edit.html"
    fields = ["name"]
    success_url = reverse_lazy("category-list")
    success_message = "✏️ Category updated successfully!"


class CategoryDeleteView(MessageDeleteMixin, DeleteView):
    model = Category
    template_name = "tracker/categories/delete.html"
    success_url = reverse_lazy("category-list")
    success_message = "🗑 Category deleted."


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
