from django import forms

class SavingPlanForm(forms.Form):
    target_amount = forms.DecimalField(label="Target Amount (INR)", max_digits=15, decimal_places=2)
    monthly_savings = forms.DecimalField(label="Monthly Savings (INR)", max_digits=10, decimal_places=2)
    expected_rate_of_return = forms.DecimalField(label="Expected Rate of Return (%)", max_digits=5, decimal_places=2)
    years_to_save = forms.IntegerField(label="Years to Save", min_value=1)
