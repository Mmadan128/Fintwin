from django.shortcuts import render
from django.http import HttpResponseServerError
from .models import RetirementGoal, WhatIfScenario

def retirement_goal_view(request):
    try:
        goal = None
        what_if_scenarios = []
        scenario_results = {}

        # Handle form submission
        if request.method == 'POST':
            # Retrieve form data from POST request
            target_amount = float(request.POST.get('target_amount'))
            current_savings = float(request.POST.get('current_savings'))
            monthly_savings = float(request.POST.get('monthly_savings'))
            investment_return_rate = float(request.POST.get('investment_return_rate'))
            target_age = int(request.POST.get('target_age'))
            current_age = int(request.POST.get('current_age'))

            # Create the RetirementGoal instance and save to DB
            goal = RetirementGoal.objects.create(
                target_amount=target_amount,
                current_savings=current_savings,
                monthly_savings=monthly_savings,
                investment_return_rate=investment_return_rate,
                target_age=target_age,
                current_age=current_age
            )

            # Create investment scenarios
            create_investment_scenarios(goal)

            # Create what-if scenarios based on the goal
            create_whatif_scenarios(goal)

            # Retrieve all scenarios for display
            what_if_scenarios = WhatIfScenario.objects.filter(goal=goal)

            # Investment scenarios (fixed)
            investment_scenarios = {
                'Conservative': 0.04,  # Example return rate of 4%
                'Moderate': 0.07,  # Example return rate of 7%
                'Aggressive': 0.10  # Example return rate of 10%
            }

            # Calculate expected returns based on the scenarios
            for scenario, return_rate in investment_scenarios.items():
                future_value = calculate_future_value(
                    current_savings, monthly_savings, return_rate, target_age - current_age
                )
                scenario_results[scenario] = future_value

        # Only render goal and scenarios if the form has been submitted
        return render(request, 'simulations/retirement_goal_form.html', {
            'goal': goal,
            'what_if_scenarios': what_if_scenarios,
            'scenario_results': scenario_results
        })

    except Exception as e:
        print(f"Error: {e}")
        return HttpResponseServerError(f"An error occurred: {e}")

def create_investment_scenarios(goal):
    """Generate investment scenarios like Conservative, Moderate, and Aggressive"""
    investment_scenarios = {
        'Conservative': 0.04,  # Example return rate of 4%
        'Moderate': 0.07,  # Example return rate of 7%
        'Aggressive': 0.10  # Example return rate of 10%
    }

    for scenario_name, return_rate in investment_scenarios.items():
        future_value = calculate_future_value(
            goal.current_savings, goal.monthly_savings, return_rate, goal.target_age - goal.current_age
        )
        WhatIfScenario.objects.create(goal=goal, scenario_name=scenario_name, future_value=future_value)

def create_whatif_scenarios(goal):
    """Generate What-If Scenarios with correctly adjusted inflation rates"""
    inflation_scenarios = {
        'No Inflation': 0.00,  # No inflation impact
        'Low Inflation': 0.02,  # 2% inflation
        'High Inflation': 0.05  # 5% inflation
    }

    for scenario_name, inflation_rate in inflation_scenarios.items():
        future_value = calculate_future_value(
            goal.current_savings, goal.monthly_savings, goal.investment_return_rate, goal.target_age - goal.current_age
        )
        
        # Properly adjust for inflation
        adjusted_future_value = adjust_for_inflation(future_value, inflation_rate, goal.target_age - goal.current_age)

        WhatIfScenario.objects.create(
            goal=goal, scenario_name=scenario_name, future_value=round(adjusted_future_value, 2)
        )


def calculate_future_value(current_savings, monthly_savings, annual_rate_of_return, years):
    """Calculate future value with compound interest and monthly contributions"""
    months = years * 12
    monthly_rate = annual_rate_of_return / 12
    
    # If the adjusted rate is negative or zero, prevent math errors
    if monthly_rate > 0:
        future_value = current_savings * (1 + monthly_rate) ** months
        future_value += monthly_savings * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    else:
        future_value = current_savings + (monthly_savings * months)  # Simple sum if negative return

    return round(future_value, 2)  # Return a rounded value
import math
def adjust_for_inflation(future_value, inflation_rate, years):
    """Adjust future value for inflation properly"""
    return future_value / math.pow(1 + inflation_rate, years)
