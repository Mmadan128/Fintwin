def tax_calculation(income):
    # Define the new tax slabs for FY 2025-26
    tax_slabs = [
        (400000, 0),        # Up to ₹4,00,000 - No tax
        (800000, 0.05),     # ₹4,00,001 to ₹8,00,000 - 5%
        (1200000, 0.10),    # ₹8,00,001 to ₹12,00,000 - 10%
        (1600000, 0.15),    # ₹12,00,001 to ₹16,00,000 - 15%
        (2000000, 0.20),    # ₹16,00,001 to ₹20,00,000 - 20%
        (2400000, 0.25),    # ₹20,00,001 to ₹24,00,000 - 25%
        (float('inf'), 0.30) # Above ₹24,00,000 - 30%
    ]

    tax = 0
    prev_limit = 0
    for limit, rate in tax_slabs:
        if income > prev_limit:
            taxable_income = min(income, limit) - prev_limit
            tax += taxable_income * rate
            prev_limit = limit
        else:
            break

    # Apply Section 87A Rebate if eligible (income <= ₹12,00,000)
    if income <= 1200000:
        tax_rebate = 60000
        tax = max(0, tax - tax_rebate)
    else:
        tax_rebate = 0

    return tax

from .models import Expense

# Remove all records from YourModel table
Expense.objects.all().delete()
