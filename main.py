import locale
import pandas as pd
import matplotlib.pyplot as plt

#Replace the locale with Brazil to change how numbers are shown.
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Load the CSV file into a DataFrame
def load_data(file_path):
    df = pd.read_csv(
        file_path,
        sep=',',
        thousands='.',
        decimal=',',
        parse_dates=['Date']
    )
    df = df.sort_values(by='Date')
    df['Month'] = df['Date'].dt.to_period('M')
    return df

def add_type_column(df):
    df['Type'] = df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')
    return df

def filter_year(df, year):
    return df[(df['Date'] >= f'{year}-01-01') & (df['Date'] < f'{year+1}-01-01')].copy()

def summarize_by_category(df):
    return df.groupby('Category')['Amount'].sum().reset_index(name='TotalAmount')

def summarize_monthly_totals(df):
    monthly_totals = df.groupby('Month')['Amount'].sum()
    monthly_totals.index = monthly_totals.index.to_timestamp()
    return monthly_totals

def plot_monthly_totals(monthly_data, year):
    """
    Plots a line chart of monthly totals for the specified year
    """
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_data.index, monthly_data.values, marker='o', linestyle='-')
    plt.title(f'Monthly Totals ({year})')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_category_totals(category_data, year):
    """"
    Plots a bar chart of total amounts by category for the specified year
    """
    plt.figure(figsize=(12, 8))
    plt.bar(category_data.index, category_data.values, color='skyblue')
    plt.title(f'Totals by Category ({year})')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

df = load_data('/Users/henriqueamorim/Henrique/finance_tracker/transactions.csv')

df = add_type_column(df)

#Sort the dataframe by date
print(df.head())

print("Data Info:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())

#Setting a dataframe only for 2023
df_2023 = filter_year(df, 2023)

#Group by Monthly Totals
monthly_totals_2023 = summarize_monthly_totals(df_2023)
print("\nMonthly Total:")
print(monthly_totals_2023)

#Group by category and sum
category_totals_2023 = summarize_by_category(df_2023)
print("\nExpenses by Category:")
print(category_totals_2023)

#Making the graph for monthly totals
plot_monthly_totals(monthly_totals_2023, 2023)

#Making the graph for the category spending
plot_category_totals(category_totals_2023, 2023)

#Seeing the differences between Income and Expenses
totals_by_type_2023 = df_2023.groupby('Type')['Amount'].sum()
print(totals_by_type_2023)