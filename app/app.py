#This application is built by dzikamai matereke
#Github: 
#linkedin:  
#This is built as my 2021 Complete Python Bootcamp From Zero to Hero in Python capstone project
'''this is build using the following libraries: 
streamlit: https://streamlit.io/ an opem source platform for creating and sharing custom web apps for machine learning and data science with python.
plotly.graph_objects: https://plotly.com/python-api-reference/generated/plotly.graph_objects.Bar.html#id5 a graphing library for creating charts and graphics. very powerful
numpy: https://numpy.org/doc/stable/reference/index.html for performing mathematical equations
google search api: https://pypi.org/project/googlesearch-python/ for querying tax rates
'''
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from googlesearch import search

#setting the page title and heading for the webapp
st.set_page_config(page_title="Savings Calculator")
st.title("Savings Calculator")

#Headers
st.header("**Monthly Income**")
st.subheader("Salary")

#creating columns: https://docs.streamlit.io/en/stable/api.html?highlight=beta_columns#streamlit.beta_columns
#colAnnualSal = columnn object named colAnnual Salary
colAnnualSal, colTax = st.beta_columns(2)

#using the with context manager to manager external resources. auto handling of setup and teardown phases:https://realpython.com/python-with-statement/
with colAnnualSal:
    salary = st.number_input("Enter your annual salary($): ", min_value=0.0, format='%f')
with colTax:
    #calculate tax rate based of location
    #I need to find an api that can search for query with location + income and gives you tax rate
    results = st.number_input("Enter your tax rate ($): ", min_value=0.0, format='%f')
        
tax_rate = results/100.0
salary_after_taxes = salary * (1 - tax_rate)
monthly_takehome_salary = round(salary_after_taxes / 12.0, 2)

st.header("**Monthly Expenses**")
colExpenses1, colExpenses2 = st.beta_columns(2)

with colExpenses1:
    st.subheader("Monthly Rental")
    monthly_rental = st.number_input("Enter your monthly rental($): ", min_value=0.0,format='%f' )
    
    st.subheader("Daily Food Budget")
    daily_food = st.number_input("Enter your daily food budget ($): ", min_value=0.0,format='%f' )
    monthly_food = daily_food * 30
    
    st.subheader("Monthly Unforeseen Expenses")
    monthly_unforeseen = st.number_input("Enter your monthly unforeseen expenses ($): ", min_value=0.0,format='%f' ) 
    
with colExpenses2:
    st.subheader("Monthly Transport")
    monthly_transport = st.number_input("Enter your monthly transport fee ($): ", min_value=0.0,format='%f' )   
    
    st.subheader("Monthly Utilities Fees")
    monthly_utilities = st.number_input("Enter your monthly utilities fees ($): ", min_value=0.0,format='%f' )
    
    st.subheader("Monthly Entertainment Budget")
    monthly_entertainment = st.number_input("Enter your monthly entertainment budget ($): ", min_value=0.0,format='%f' )   

monthly_expenses = monthly_rental + monthly_food + monthly_transport + monthly_entertainment + monthly_utilities + monthly_unforeseen
monthly_savings = monthly_takehome_salary - monthly_expenses


st.header("**Savings**")
st.subheader("Monthly Take Home Salary: $" + str(round(monthly_takehome_salary,2)))
st.subheader("Monthly Expenses: $" + str(round(monthly_expenses, 2)))
st.subheader("Monthly Savings: $" + str(round(monthly_savings, 2)))

st.markdown("---")

st.header("**Forecast of your savings Savings**")
colForecast1, colForecast2 = st.beta_columns(2)
with colForecast1:
    st.subheader("Number of years to forecast")
    forecast_year = st.number_input("How many years to forecast (Min 1 year): ", min_value=0,format='%d')
    forecast_months = 12 * forecast_year 
    
    st.subheader("Annual Inflation Rate")
    annual_inflation = st.number_input("Enter annual inflation rate (%): ", min_value=0.0,format='%f')
    monthly_inflation = (1+annual_inflation)**(1/12) - 1
    cumulative_inflation_forecast = np.cumprod(np.repeat(1 + monthly_inflation, forecast_months))
    forecast_expenses = monthly_expenses*cumulative_inflation_forecast
    
with colForecast2:
    st.subheader("Annual Salary Growth Rate")
    annual_growth = st.number_input("Enter your expected annual salary growth (%): ", min_value=0.0,format='%f')
    monthly_growth = (1 + annual_growth) ** (1/12) - 1
    cumulative_salary_growth = np.cumprod(np.repeat(1 + monthly_growth, forecast_months))
    forecast_salary = monthly_takehome_salary * cumulative_salary_growth 
    
forecast_savings = forecast_salary - forecast_expenses 
cumulative_savings = np.cumsum(forecast_savings)

x_values = np.arange(forecast_year + 1)

fig = go.Figure()
fig.add_trace(
        go.Scatter(
            x=x_values, 
            y=forecast_salary,
            name="Forecast Salary"
        )
    )

fig.add_trace(
        go.Scatter(
            x=x_values,
            y=forecast_expenses,
            name= "Forecast Expenses"
        )
    )

fig.add_trace(
        go.Scatter(
                x=x_values, 
                y=cumulative_savings,
                name= "Forecast Savings"
            )
    )
fig.update_layout(title='Forecast Salary, Expenses & Savings Over the Years',
                   xaxis_title='Year',
                   yaxis_title='Amount($)')

st.plotly_chart(fig, use_container_width=True)
