import locale
import pandas as pd
import matplotlib.pyplot as plt

#Replace the locale with Brazil to change how numbers are shown.
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Load the CSV file into a DataFrame
df = pd.read_csv(
    'transactions.csv',
    sep=',',
    thousands='.',
    decimal=',',
    parse_dates=['Date']
)

#Sort the dataframe by date
df = df.sort_values(by='Date')
print(df.head())

print("Data Info:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())

#Creating the Month column
df['Month'] = df['Date'].dt.to_period('M')

#Setting a dataframe only for 2023
df_2023 = df[(df['Date'] >= '2023-01-01') & (df['Date'] < '2024-01-01')].copy()

#Group by category and sum
category_totals = df_2023.groupby('Category')['Amount'].sum()
print("\nExpenses by Category:")
print(category_totals)

#Group by Monthly Totals
monthly_totals = df_2023.groupby('Month')['Amount'].sum()
print("\nMonthly Total:")
print(monthly_totals)

#Making the graph for monthly totals
##Convert to Timestamp to help with plotting
monthly_totals.index = monthly_totals.index.to_timestamp()

##plot(x-axis, y-axis, marker adds a circle to each data point)
plt.plot(monthly_totals.index, monthly_totals.values, marker='o')

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
##Converting category_totals into a df with two columns: Category and TotalAmount
cat_df = category_totals.reset_index(name='TotalAmount')

##Same graph commands as before
plt.bar(cat_df['Category'], cat_df['TotalAmount'], color='skyblue')
plt.title('Totals by Category (2023)')
plt.xlabel('Category')
plt.ylabel('Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Separating income from expenses
df_2023['Type'] = df_2023['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')

##Seeing 
totals_by_type = df_2023.groupby('Type')['Amount'].sum()
print(totals_by_type)