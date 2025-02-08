from django.urls import path
from . import views  # Import views from the same app

urlpatterns = [
    path('finance-news/', views.get_finance_news, name='finance_news'),
]
