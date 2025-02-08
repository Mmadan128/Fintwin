# simulations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('retirement-goal/', views.retirement_goal_view, name='retirement_goal'),
]
