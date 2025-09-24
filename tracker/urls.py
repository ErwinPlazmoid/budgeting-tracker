from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.HomeView.as_view(), name="home"),
    # Transactions
    path("transactions/", views.TransactionListView.as_view(), name="transaction-list"),
    path("transactions/add/", views.TransactionCreateView.as_view(), name="transaction-add"),
    path("transactions/<int:pk>/edit/", views.TransactionUpdateView.as_view(), name="transaction-edit"),
    path("transactions/<int:pk>/delete/", views.TransactionDeleteView.as_view(), name="transaction-delete"),
    # Categories
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("categories/add/", views.CategoryCreateView.as_view(), name="category-add"),
    path("categories/<int:pk>/edit/", views.CategoryUpdateView.as_view(), name="category-edit"),
    path("categories/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category-delete"),
    # Analytics
    path("analytics/", views.AnalyticsHomeView.as_view(), name="analytics-home"),
    path("analytics/summary/", views.AnalyticsSummaryView.as_view(), name="analytics-summary"),
    path("analytics/monthly/", views.AnalyticsMonthlyView.as_view(), name="analytics-monthly"),
    path("analytics/categories/", views.AnalyticsCategoriesView.as_view(), name="analytics-categories"),
]

