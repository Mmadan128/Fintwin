# simulations/forms.py
from django import forms
from .models import Expense

class RetirementGoalForm(forms.Form):
    target_age = forms.IntegerField(required=True, label="Target Age")
    current_age = forms.IntegerField(required=True, label="Current Age")
    monthly_contribution = forms.FloatField(required=True, label="Monthly Contribution (in INR)")
    expected_rate_of_return = forms.FloatField(required=True, label="Expected Rate of Return (%)")
    retirement_expenses = forms.FloatField(required=True, label="Expected Monthly Retirement Expenses (in INR)")
    inflation_rate = forms.FloatField(required=True, label="Inflation Rate (%)")

class FinancialDataForm(forms.Form):
    income = forms.DecimalField(label="Income (INR)", max_digits=10, decimal_places=2)
    monthly_contribution = forms.DecimalField(label="Monthly Contribution (INR)", max_digits=10, decimal_places=2)
    expected_rate_of_return = forms.DecimalField(label="Expected Rate of Return (%)", max_digits=5, decimal_places=2)
    target_age = forms.IntegerField(label="Target Age")
    current_age = forms.IntegerField(label="Current Age")
    expected_monthly_retirement_expenses = forms.DecimalField(label="Expected Monthly Retirement Expenses (INR)", max_digits=10, decimal_places=2)
    inflation_rate = forms.DecimalField(label="Inflation Rate (%)", max_digits=5, decimal_places=2)


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }    
from .models import RiskAssessment

class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['age', 'income', 'investment_experience', 'financial_goals', 'risk_tolerance']
        widgets = {
            'financial_goals': forms.Textarea(attrs={'rows': 3}),
        }

class SavingPlanForm(forms.Form):
    target_amount = forms.DecimalField(label="Target Amount (INR)", max_digits=15, decimal_places=2)
    monthly_savings = forms.DecimalField(label="Monthly Savings (INR)", max_digits=10, decimal_places=2)
    expected_rate_of_return = forms.DecimalField(label="Expected Rate of Return (%)", max_digits=5, decimal_places=2)
    years_to_save = forms.IntegerField(label="Years to Save", min_value=1)

class StockForm(forms.Form):
    stock_symbols = forms.CharField(label='Stock Symbols (comma separated)', max_length=200)