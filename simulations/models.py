# models.py

from django.db import models

class RetirementGoal(models.Model):
    target_amount = models.FloatField()
    current_savings = models.FloatField()
    monthly_savings = models.FloatField()
    investment_return_rate = models.FloatField()
    target_age = models.IntegerField()
    current_age = models.IntegerField()

    def __str__(self):
        return f"Retirement Goal for Age {self.target_age}"

class WhatIfScenario(models.Model):
    goal = models.ForeignKey(RetirementGoal, on_delete=models.CASCADE)
    scenario_name = models.CharField(max_length=100)
    future_value = models.FloatField()

    def __str__(self):
        return f"Scenario: {self.scenario_name} for Goal {self.goal.target_age}"
