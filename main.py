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

#Group by category and sum
category_totals_2023 = summarize_by_category(df_2023)
print("\nExpenses by Category:")
print(category_totals_2023)

#Group by Monthly Totals
monthly_totals_2023 = summarize_monthly_totals(df_2023)
print("\nMonthly Total:")
print(monthly_totals_2023)

#Making the graph for monthly totals
    ##plot(x-axis, y-axis, marker adds a circle to each data point)
plt.plot(monthly_totals_2023.index, monthly_totals_2023.values, marker='o')

    ##Names for the graph title and axis
plt.title('Monthly Totals (2023)')
plt.xlabel('Month')
plt.ylabel('Amount')

    ##Rotates the labels of the x-axis to improve readability
plt.xticks(rotation=45)

    ##Adjusts the layout for better fit
plt.tight_layout()

    ##Display the graph
plt.show()

#Making the graph for the category spending
    ##Same graph commands as before
plt.bar(category_totals_2023['Category'], category_totals_2023['TotalAmount'], color='skyblue')
plt.title('Totals by Category (2023)')
plt.xlabel('Category')
plt.ylabel('Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Seeing the differences between Income and Expenses
totals_by_type_2023 = df_2023.groupby('Type')['Amount'].sum()
print(totals_by_type_2023)