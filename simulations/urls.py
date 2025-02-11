from django.urls import path
from . import views

urlpatterns = [
    path('retirement_goal/', views.retirement_goal, name='retirement_goal'),
    path('financial_dashboard/', views.financial_dashboard, name='financial_dashboard'),
    path('tax_calculation/', views.tax_calculation, name='tax_calculation'),
    path('saving_plans/', views.saving_plans, name='saving_plans'),
    path('expense_tracker/', views.expense_tracker, name='expense_tracker'),
    path('risk_assessment/', views.risk_assessment, name='risk_assessment'),
   path('market_data/', views.market_data, name='market_data'),
    path('financegpt/', views.financegpt_view, name='financegpt_view'),
]
