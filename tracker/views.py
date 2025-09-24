from django.shortcuts import render
from django.views.generic import TemplateView

# Home
class HomeView(TemplateView):
    template_name = "tracker/home.html"


# Transactions
class TransactionListView(TemplateView):
    template_name = "tracker/transactions/list.html"

class TransactionCreateView(TemplateView):
    template_name = "tracker/transactions/add.html"

class TransactionUpdateView(TemplateView):
    template_name = "tracker/transactions/edit.html"

class TransactionDeleteView(TemplateView):
    template_name = "tracker/transactions/delete.html"


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
