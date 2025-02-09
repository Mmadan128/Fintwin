from django.db import models

class RetirementGoal(models.Model):
    current_age = models.IntegerField()
    target_age = models.IntegerField()
    current_savings = models.FloatField()
    monthly_savings = models.FloatField()
    investment_return_rate = models.FloatField()
    target_amount = models.FloatField()  # This stores the calculated future value


class WhatIfScenario(models.Model):  # Add this if needed
    name = models.CharField(max_length=100)
    return_rate = models.FloatField()
    retirement_goal = models.ForeignKey(RetirementGoal, on_delete=models.CASCADE)
from django import forms

class FinancialDataForm(forms.Form):
    income = forms.DecimalField(label="Income (INR)", max_digits=10, decimal_places=2)
    monthly_contribution = forms.DecimalField(label="Monthly Contribution (INR)", max_digits=10, decimal_places=2)
    expected_rate_of_return = forms.DecimalField(label="Expected Rate of Return (%)", max_digits=5, decimal_places=2)
    target_age = forms.IntegerField(label="Target Age")
    current_age = forms.IntegerField(label="Current Age")
    expected_monthly_retirement_expenses = forms.DecimalField(label="Expected Monthly Retirement Expenses (INR)", max_digits=10, decimal_places=2)
    inflation_rate = forms.DecimalField(label="Inflation Rate (%)", max_digits=5, decimal_places=2)

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]
    
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return f"{self.description} - {self.amount} ({self.category})"    
    
class RiskAssessment(models.Model):
    # Add a max_length of 20 for the investment_experience field to accommodate the longest choice.
    INVESTMENT_EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    RISK_TOLERANCE_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    age = models.IntegerField()
    income = models.FloatField()
    investment_experience = models.CharField(
        max_length=20,  # Increased max_length to accommodate longest choice
        choices=INVESTMENT_EXPERIENCE_CHOICES,
    )
    financial_goals = models.TextField()
    risk_tolerance = models.CharField(
        max_length=10, 
        choices=RISK_TOLERANCE_CHOICES
    )
    risk_score = models.FloatField(null=True, blank=True)

    def calculate_risk(self):
        # Example logic for calculating the risk score based on user input
        if self.risk_tolerance == 'low':
            self.risk_score = 20
        elif self.risk_tolerance == 'medium':
            self.risk_score = 50
        else:
            self.risk_score = 80

        # Add more custom logic for calculating based on other factors (age, income, experience, etc.)
        self.save()

    def __str__(self):
        return f"Risk Assessment for Age: {self.age}, Income: {self.income}"