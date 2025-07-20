import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set default style
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 5)

def plot_yearly_sales(df):
    plt.figure()
    sns.lineplot(data=df, x='Year', y='EV_Sales_Quantity', estimator='sum', marker='o')
    plt.title("Total EV Sales by Year in India")
    plt.xlabel("Year")
    plt.ylabel("Sales")
    plt.tight_layout()
    return plt

def plot_monthly_sales(df):
    order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    plt.figure()
    sns.barplot(data=df, x='Month_Name', y='EV_Sales_Quantity', estimator='sum', order=order)
    plt.title("EV Sales by Month")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.tight_layout()
    return plt

def plot_top_states(df, top_n=10):
    top_states = df.groupby('State')['EV_Sales_Quantity'].sum().sort_values(ascending=False).head(top_n)
    plt.figure()
    top_states.plot(kind='bar')
    plt.title(f'Top {top_n} States by EV Sales')
    plt.ylabel('Sales')
    plt.xlabel('State')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt

def plot_by_vehicle_category(df):
    plt.figure()
    sns.barplot(x='Vehicle_Category', y='EV_Sales_Quantity', data=df, estimator='sum')
    plt.title("EV Sales by Vehicle Category")
    plt.xticks(rotation=0)
    plt.tight_layout()
    return plt

def plot_by_vehicle_type(df):
    plt.figure(figsize=(12, 5))
    sns.barplot(x='Vehicle_Type', y='EV_Sales_Quantity', data=df, estimator='sum')
    plt.title("EV Sales by Vehicle Type")
    plt.xticks(rotation=90)
    plt.tight_layout()
    return plt
