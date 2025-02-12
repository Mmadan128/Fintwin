# simulations/views.py
from django.shortcuts import render, redirect
from .forms import RetirementGoalForm,FinancialDataForm,ExpenseForm,RiskAssessmentForm,SavingPlanForm,StockForm
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import io
import pandas as pd
from .tax_calculation import tax_calculation
from .models import FinancialDataForm,Expense,RiskAssessment
import yfinance as yf
import requests
import openai
from django.conf import settings 
from .utils import get_stock_data

def generate_ai_advice(target_age, current_age, monthly_contribution, expected_rate_of_return, retirement_expenses, inflation_rate):
    openai.api_key = settings.OPENAI_API_KEY

    # Formatting prompt 
    messages = [
        {"role": "system", "content": "You are a financial advisor."},
        {"role": "user", "content": f"""
        Given the following information:
        Target retirement age: {target_age}
        Current age: {current_age}
        Monthly contribution: {monthly_contribution} INR
        Expected rate of return: {expected_rate_of_return * 100}% annually
        Estimated retirement expenses: {retirement_expenses} INR annually
        Inflation rate: {inflation_rate * 100}%

        Please provide personalized financial advice.
        Give answers in an easy language ,in points ,in visually good way and give tab after each point
        """}
    ]

    # Make the API call to get AI-generated advice
    response = client.chat.completions.create(
        model="gpt-4",  # Choose the model you need
        messages=messages,
        max_tokens=500  # Adjust as necessary
    )

    # Extract advice from response
    ai_advice = response.choices[0].message.content.strip()


    return ai_advice

def retirement_goal(request):
    chart_url = None
    future_value = None
    adjusted_expenses = None
    ai_advice = None

    if request.method == 'POST':
        form = RetirementGoalForm(request.POST)
        if form.is_valid():
            # Get form data
            target_age = form.cleaned_data['target_age']
            current_age = form.cleaned_data['current_age']
            monthly_contribution = form.cleaned_data['monthly_contribution']
            expected_rate_of_return = form.cleaned_data['expected_rate_of_return'] / 100
            retirement_expenses = form.cleaned_data['retirement_expenses']
            inflation_rate = form.cleaned_data['inflation_rate'] / 100

            # Calculate the number of years to retirement
            years_to_retirement = target_age - current_age
            future_value = 0
            savings_over_time = []

            # Calculate future value of retirement fund with monthly contributions
            for age in range(current_age, target_age + 1):
                future_value += monthly_contribution * 12  # Annual contribution
                future_value *= (1 + expected_rate_of_return)  # Growth for the year

                # Record projected savings for each year
                savings_over_time.append((age, future_value))

            # Calculate adjusted retirement expenses considering inflation
            adjusted_expenses = retirement_expenses * (1 + inflation_rate) ** years_to_retirement

            # Generate AI advice based on the form data
            ai_advice = generate_ai_advice(target_age, current_age, monthly_contribution, expected_rate_of_return, retirement_expenses, inflation_rate)

            # Convert the savings_over_time for graphing
            ages = [x[0] for x in savings_over_time]
            values = [x[1] for x in savings_over_time]

            # Plotting the chart
            fig, ax = plt.subplots()
            ax.plot(ages, values, label="Projected Savings")
            ax.set(xlabel='Age', ylabel='Savings (INR)',
                   title='Projected Savings Over Time')
            ax.grid(True)
            plt.tight_layout()

            # Convert the plot to a PNG image for embedding in the page
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            chart_url = base64.b64encode(buf.read()).decode('utf-8')

    else:
        form = RetirementGoalForm()

    return render(request, 'simulations/retirement_goal.html', {
        'form': form,
        'chart_url': chart_url,
        'future_value': future_value,
        'adjusted_expenses': adjusted_expenses,
        'ai_advice': ai_advice,  # Add AI advice to context
    })

def calculate_tax(income):
    # New income tax slabs for FY 2025-26 (AY 2026-27)
    slabs = [
        (4000000, 0),   # 0% tax for income up to 4 lakh
        (6000000, 0.05), # 5% tax for income above 4 lakh and up to 6 lakh
        (9000000, 0.1),  # 10% tax for income above 6 lakh and up to 9 lakh
        (12000000, 0.2), # 20% tax for income above 9 lakh and up to 12 lakh
        (15000000, 0.3), # 30% tax for income above 12 lakh
    ]

    tax = 0
    previous_limit = 0

    for limit, rate in slabs:
        if income > previous_limit:
            taxable_income = min(income, limit) - previous_limit
            tax += taxable_income * rate
            previous_limit = limit
        else:
            break

    return tax

# Financial Dashboard View


def get_stock_price(symbol="AAPL"):
    """
    Fetch the real-time stock price using yfinance (you can change the stock symbol here).
    """
    stock = yf.Ticker(symbol)
    stock_data = stock.history(period="1d")
    return stock_data['Close'].iloc[-1]

def get_crypto_price(crypto_id="bitcoin"):
    """
    Fetch the real-time cryptocurrency price using CoinGecko API (default: Bitcoin).
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=inr"
    response = requests.get(url)
    data = response.json()
    return data[crypto_id]['inr']



# List of stock symbols (NSE stocks in this case)
stock_symbols = [
    'HINDUNILVR.NS',  # Hindustan Unilever
    'RELIANCE.NS',     # Reliance Industries
    'INFY.NS',         # Infosys
    'LT.NS',           # Larsen & Toubro
    'HDFCBANK.NS',     # HDFC Bank
    'ICICIBANK.NS',    # ICICI Bank
    'TCS.NS',          # Tata Consultancy Services
    'SBIN.NS',         # State Bank of India
    'BAJFINANCE.NS',   # Bajaj Finance
    'ITC.NS',          # ITC Ltd.
    'KOTAKBANK.NS',    # Kotak Mahindra Bank
    'AXISBANK.NS',     # Axis Bank
    'MARUTI.NS',       # Maruti Suzuki
    'WIPRO.NS',        # Wipro
    'M&M.NS'           # Mahindra & Mahindra
]

def stock_view(request):
    gainers, losers = [], []
    
    # Check if the request method is POST and user has submitted symbols
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock_symbols = form.cleaned_data['stock_symbols']  # Assume it's a comma-separated string of symbols
            symbols_list = stock_symbols.split(',')
            gainers, losers = get_stock_data(symbols_list)  # Fetch stock data
    else:
        form = StockForm()

    return render(request, 'stock_data.html', {
        'form': form,
        'gainers': gainers,
        'losers': losers,
    })
# Generate a chart for market overview (Gainers vs Losers)
def plot_market_overview(gainers, losers):
    labels = ['Top Gainers', 'Top Losers']
    sizes = [len(gainers), len(losers)]
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_data = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return image_data


def market_data(request):
    # Fetching the data for top gainers and losers
    try:
        # Get top gainers and losers from NSE (India) using Yahoo Finance
        nse_top_gainers = yf.download('^NSEBANK', period='1d')  # Sample for Nifty Bank, you can adjust
        nse_top_losers = yf.download('^NSEAUTO', period='1d')   # Sample for Nifty Auto, adjust as necessary
        
        # Ensure that the data has been returned
        if not nse_top_gainers.empty and not nse_top_losers.empty:
            # Convert data to DataFrame
            gainers_data = pd.DataFrame(nse_top_gainers)
            losers_data = pd.DataFrame(nse_top_losers)
        else:
            # Handle the case where data was not found or fetched
            gainers_data = None
            losers_data = None
    except Exception as e:
        gainers_data = None
        losers_data = None
        error_message = str(e)

    # Render the template with the data
    return render(
        request,
        "simulations/market_data.html",
        {
            "gainers_data": gainers_data,
            "losers_data": losers_data,
            "error_message": error_message if 'error_message' in locals() else None,
        },
    )


def financial_dashboard(request):
    tax = 0
    financial_data = None
    image_data = None
    stock_price = None
    crypto_price = None

    if request.method == "POST":
        form = FinancialDataForm(request.POST)
        if form.is_valid():
            # Extract form data
            income = form.cleaned_data["income"]
            target_age = form.cleaned_data["target_age"]
            current_age = form.cleaned_data["current_age"]
            monthly_contribution = form.cleaned_data["monthly_contribution"]
            expected_rate_of_return = form.cleaned_data["expected_rate_of_return"]
            expected_monthly_retirement_expenses = form.cleaned_data["expected_monthly_retirement_expenses"]
            inflation_rate = form.cleaned_data["inflation_rate"]

            # Perform tax calculation
            tax = calculate_tax(income)

            # Financial Data Dictionary
            financial_data = {
                'income': income,
                'target_age': target_age,
                'current_age': current_age,
                'monthly_contribution': monthly_contribution,
                'expected_rate_of_return': expected_rate_of_return,
                'expected_monthly_retirement_expenses': expected_monthly_retirement_expenses,
                'inflation_rate': inflation_rate,
            }

            # Projected Savings Over Time
            years_to_retirement = target_age - current_age
            ages = [current_age + i for i in range(years_to_retirement + 1)]
            projected_savings = []

            # Calculate projected savings over time with compound interest
            current_savings = 0
            for age in ages:
                current_savings = current_savings * (1 + expected_rate_of_return / 100) + monthly_contribution * 12
                projected_savings.append(current_savings)

            # Plotting the savings over time
            fig, ax = plt.subplots()
            ax.plot(ages, projected_savings, label="Projected Savings")
            ax.set_xlabel('Age')
            ax.set_ylabel('Savings (INR)')
            ax.set_title('Projected Retirement Savings Over Time')

            # Save plot to a PNG image in memory
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            image_data = base64.b64encode(buf.read()).decode("utf-8")
            buf.close()

            # Fetch real-time stock and crypto prices
            stock_price = get_stock_price("AAPL")  # Example for Apple stock
            crypto_price = get_crypto_price("bitcoin")  # Example for Bitcoin

    else:
        form = FinancialDataForm()

    return render(
        request,
        "simulations/financial_dashboard.html",
        {
            "form": form,
            "tax": tax,
            "financial_data": financial_data,
            "image_data": image_data,
            "stock_price": stock_price,
            "crypto_price": crypto_price,
        },
    )




def tax_calculation(request):
    if request.method == 'POST':
        try:
            # Get the income entered by the user
            income = float(request.POST.get('income'))

            # Define the new tax slabs for FY 2025-26 (Assessment Year 2026-27)
            tax_slabs = [
                (400000, 0),        # Up to ₹4,00,000 - No tax
                (800000, 0.05),     # ₹4,00,001 to ₹8,00,000 - 5%
                (1200000, 0.10),    # ₹8,00,001 to ₹12,00,000 - 10%
                (1600000, 0.15),    # ₹12,00,001 to ₹16,00,000 - 15%
                (2000000, 0.20),    # ₹16,00,001 to ₹20,00,000 - 20%
                (2400000, 0.25),    # ₹20,00,001 to ₹24,00,000 - 25%
                (float('inf'), 0.30) # Above ₹24,00,000 - 30%
            ]

            # Calculate tax for the given income
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

            # Send data to the template
            return render(request, 'simulations/tax_calculation.html', {
                'income': income,
                'tax': tax,
                'tax_rebate': tax_rebate
            })

        except ValueError:
            # Handle invalid input
            return render(request, 'simulations/tax_calculation.html', {
                'error': "Please enter a valid income."
            })

    return render(request, 'simulations/tax_calculation.html')


def calculate_savings(target_amount, monthly_savings, expected_rate_of_return, years_to_save):
    months_to_save = years_to_save * 12
    savings = 0
    monthly_rate_of_return = expected_rate_of_return / 100 / 12
    savings_over_time = []

    for month in range(1, months_to_save + 1):
        savings += monthly_savings
        savings *= (1 + monthly_rate_of_return)  # Apply monthly compounded interest
        savings_over_time.append(savings)

        if savings >= target_amount:
            break

    return savings_over_time, savings, month


# Saving Plans View
def saving_plans(request):
    savings_over_time = []
    final_savings = 0
    months_taken = 0
    form = SavingPlanForm()

    if request.method == "POST":
        form = SavingPlanForm(request.POST)
        if form.is_valid():
            # Extract form data
            target_amount = form.cleaned_data["target_amount"]
            monthly_savings = form.cleaned_data["monthly_savings"]
            expected_rate_of_return = form.cleaned_data["expected_rate_of_return"]
            years_to_save = form.cleaned_data["years_to_save"]

            # Calculate the savings plan
            savings_over_time, final_savings, months_taken = calculate_savings(
                target_amount, monthly_savings, expected_rate_of_return, years_to_save
            )

            # Generate a plot for savings over time
            months = [i for i in range(1, months_taken + 1)]
            fig, ax = plt.subplots()
            ax.plot(months, savings_over_time, label="Cumulative Savings", color="b")
            ax.set_xlabel("Months")
            ax.set_ylabel("Savings (INR)")
            ax.set_title("Saving Plan Over Time")
            ax.legend()

            # Save plot to a PNG image in memory
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            image_data = base64.b64encode(buf.read()).decode("utf-8")
            buf.close()

            return render(
                request,
                "simulations/saving_plans.html",
                {
                    "form": form,
                    "final_savings": final_savings,
                    "months_taken": months_taken,
                    "image_data": image_data,
                },
            )

    return render(request, "simulations/saving_plans.html", {"form": form})




def expense_tracker(request):
    # Handle the form submission
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_tracker')  # Redirect to the same page after submission
    
    # Display the expenses
    expenses = Expense.objects.all()
    total_expenses = sum(expense.amount for expense in expenses)
    
    form = ExpenseForm()
    
    return render(request, 'simulations/expense_tracker.html', {
        'form': form,
        'expenses': expenses,
        'total_expenses': total_expenses
    })


def risk_assessment(request):
    risk_assessment = None
    if request.method == 'POST':
        form = RiskAssessmentForm(request.POST)
        if form.is_valid():
            # Save the form and calculate risk score
            risk_assessment = form.save()
            risk_assessment.calculate_risk()
            # Pass the risk assessment object to the template
            return render(request, 'simulations/risk_assessment.html', {
                'form': form, 
                'risk_assessment': risk_assessment
            })
    else:
        form = RiskAssessmentForm()
    
    return render(request, 'simulations/risk_assessment.html', {'form': form, 'risk_assessment': risk_assessment})

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def get_financegpt_response(prompt):
    try:
        # Using the new OpenAI API method (>=1.0.0)
        response = client.chat.completions.create(
            model="gpt-4",  # Or another model like "gpt-3.5-turbo"
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a knowledgeable financial advisor. Provide clear, actionable insights "
                        "on investments, savings, and financial planning. Your responses should be "
                        "well-organized with proper indentation and bullet points where applicable. "
                        "Ensure the content is easy to read and follow."
                        "You should make sure it is visually attractive"
                        "from now on you are financegpt not chatgpt and dont say you are developed by whom"
                        "Give proper line space between points"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500,  # Increased max_tokens to allow for longer responses
            n=1,
        )
        # Extracting the response content
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"



def financegpt_view(request):
    gpt_response = None  # Initialize as None by default

    if request.method == "POST":
        gpt_prompt = request.POST.get('gpt_prompt', '').strip()
        if gpt_prompt:
            gpt_response = get_financegpt_response(gpt_prompt)
        else:
            gpt_response = "Please enter a question above."  # Only set when the form is submitted but empty

    return render(
        request,
        "simulations/financegpt.html",  # Your template file
        {
            "gpt_response": gpt_response,  # Pass the GPT response to the template
        }
    )