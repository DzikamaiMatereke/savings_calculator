#This application is built by dzikamai matereke
#Github: 
#linkedin:  
#This is built as my 2021 Complete Python Bootcamp From Zero to Hero in Python capstone project

'''This is build using the following libraries: 
streamlit: https://streamlit.io/ an opem source platform for creating and sharing custom web apps for machine learning and data science with python.
plotly.graph_objects: https://plotly.com/python-api-reference/generated/plotly.graph_objects.Bar.html#id5 a graphing library for creating charts and graphics. very powerful
numpy: https://numpy.org/doc/stable/reference/index.html for performing mathematical equations
google search api: https://pypi.org/project/googlesearch-python/ for querying tax rates
'''
import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Set the page title and heading for the web app
st.set_page_config(page_title="Savings Calculator")
st.title("Savings Calculator")

# Function to calculate monthly take-home salary
def calculate_takehome_salary(salary, tax_rate):
    salary_after_taxes = salary * (1 - tax_rate)
    return round(salary_after_taxes / 12.0, 2)

# Function to calculate monthly expenses
def calculate_monthly_expenses(rental, food, transport, utilities, entertainment, unforeseen):
    monthly_food = food * 30
    return rental + monthly_food + transport + utilities + entertainment + unforeseen

# Function to forecast savings
def forecast_savings(monthly_takehome_salary, monthly_expenses, forecast_year, annual_inflation, annual_growth):
    forecast_months = 12 * forecast_year
    monthly_inflation = (1 + annual_inflation) ** (1/12) - 1
    cumulative_inflation_forecast = np.cumprod(np.repeat(1 + monthly_inflation, forecast_months))
    forecast_expenses = monthly_expenses * cumulative_inflation_forecast

    monthly_growth = (1 + annual_growth) ** (1/12) - 1
    cumulative_salary_growth = np.cumprod(np.repeat(1 + monthly_growth, forecast_months))
    forecast_salary = monthly_takehome_salary * cumulative_salary_growth

    forecast_savings = forecast_salary - forecast_expenses
    cumulative_savings = np.cumsum(forecast_savings)
    return forecast_salary, forecast_expenses, cumulative_savings

# Headers
st.header("**Monthly Income!**")
st.subheader("Salary")

# Creating columns for input
colAnnualSal, colTax = st.columns(2)

with colAnnualSal:
    salary = st.number_input("Enter your annual salary($): ", min_value=0.0, format='%f')
with colTax:
    tax_rate = st.number_input("Enter your tax rate (%): ", min_value=0.0, format='%f') / 100.0

monthly_takehome_salary = calculate_takehome_salary(salary, tax_rate)

st.header("**Monthly Expenses**")
colExpenses1, colExpenses2 = st.columns(2)

with colExpenses1:
    monthly_rental = st.number_input("Enter your monthly rental($): ", min_value=0.0, format='%f')
    daily_food = st.number_input("Enter your daily food budget ($): ", min_value=0.0, format='%f')
    monthly_unforeseen = st.number_input("Enter your monthly unforeseen expenses ($): ", min_value=0.0, format='%f')

with colExpenses2:
    monthly_transport = st.number_input("Enter your monthly transport fee ($): ", min_value=0.0, format='%f')
    monthly_utilities = st.number_input("Enter your monthly utilities fees ($): ", min_value=0.0, format='%f')
    monthly_entertainment = st.number_input("Enter your monthly entertainment budget ($): ", min_value=0.0, format='%f')

monthly_expenses = calculate_monthly_expenses(monthly_rental, daily_food, monthly_transport, monthly_utilities, monthly_entertainment, monthly_unforeseen)
monthly_savings = monthly_takehome_salary - monthly_expenses

st.header("**Savings**")
st.subheader(f"Monthly Take Home Salary: ${monthly_takehome_salary}")
st.subheader(f"Monthly Expenses: ${monthly_expenses}")
st.subheader(f"Monthly Savings: ${monthly_savings}")

st.markdown("---")

st.header("**Forecast of your Savings**")
colForecast1, colForecast2 = st.columns(2)

with colForecast1:
    forecast_year = st.number_input("How many years to forecast (Min 1 year): ", min_value=1, format='%d')
    annual_inflation = st.number_input("Enter annual inflation rate (%): ", min_value=0.0, format='%f') / 100.0

with colForecast2:
    annual_growth = st.number_input("Enter your expected annual salary growth (%): ", min_value=0.0, format='%f') / 100.0

forecast_salary, forecast_expenses, cumulative_savings = forecast_savings(monthly_takehome_salary, monthly_expenses, forecast_year, annual_inflation, annual_growth)

x_values = np.arange(forecast_year + 1)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x_values, y=forecast_salary, name="Forecast Salary"))
fig.add_trace(go.Scatter(x=x_values, y=forecast_expenses, name="Forecast Expenses"))
fig.add_trace(go.Scatter(x=x_values, y=cumulative_savings, name="Forecast Savings"))

fig.update_layout(title='Forecast Salary, Expenses & Savings Over the Years', xaxis_title='Year', yaxis_title='Amount($)')

st.plotly_chart(fig, use_container_width=True)
